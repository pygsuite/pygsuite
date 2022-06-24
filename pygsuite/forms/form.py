from typing import TYPE_CHECKING, List, Optional

from googleapiclient.errors import HttpError

from pygsuite import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.constants import FATAL_HTTP_CODES
from pygsuite.constants import logger
from pygsuite.drive.drive_object import DriveObject
from pygsuite.enums import MimeType
from pygsuite.exceptions import FatalHttpError
from pygsuite.forms.generated.create_item_request import CreateItemRequest
from pygsuite.forms.generated.delete_item_request import DeleteItemRequest
from pygsuite.forms.generated.form import Form as BaseForm
from pygsuite.forms.generated.location import Location
from pygsuite.forms.generated.move_item_request import MoveItemRequest
from pygsuite.forms.generated.update_form_info_request import UpdateFormInfoRequest
from pygsuite.forms.generated.update_item_request import UpdateItemRequest
from pygsuite.forms.synchronizer import WatchedDictionary
from pygsuite.forms.synchronizer import WatchedList
from pygsuite.utility.decorators import retry

if TYPE_CHECKING:
    from .generated.form_settings import FormSettings
    from .generated.info import Info
    from .generated.item import Item


class Form(BaseForm, DriveObject):
    """A form on google drive."""

    _mimetype = MimeType.FORMS

    _base_url = "https://docs.google.com/forms/d/{}/edit"

    def __init__(self, id: str = None, client=None, name=None, _form=None, local: bool = False):

        if not local:
            client = client or Clients.forms_client
        self.service = client
        self.id = parse_id(id) if id else None
        DriveObject.__init__(self, id=self.id, client=client)
        BaseForm.__init__(self, object_info=_form or client.forms().get(formId=self.id).execute())
        self._change_queue: List = []
        self.auto_sync: bool = False
        self._info_cache: Optional["Info"] = None
        self._settings_cache: Optional["FormSettings"] = None
        self._items_cache: Optional[List["Item"]] = None

        def update_factory(idx, item):
            self._mutation([UpdateItemRequest(item=item, location=Location(index=idx)).wire_format])

        self.items_update_factory = update_factory

        def delete_factory(idx):
            self._mutation([DeleteItemRequest(location=Location(index=idx)).wire_format])

        self.items_delete_factory = delete_factory

        def move_factory(original_idx, new_idx):
            self._mutation(
                [
                    MoveItemRequest(
                        new_location=Location(new_idx), original_location=Location(original_idx)
                    ).wire_format
                ]
            )

        self.items_move_factory = move_factory

        def create_factory(item, idx):
            self._mutation([CreateItemRequest(item, location=Location(idx)).wire_format])

        self.items_create_factory = create_factory

    def _mutation(self, reqs, flush: bool = False):
        if not reqs:
            return None
        self._change_queue += reqs
        if flush or self.auto_sync:
            return self.flush()

    @retry(HttpError, tries=3, delay=5, backoff=3, fatal_exceptions=(FatalHttpError,))
    def batch_update(self, requests):
        try:
            return (
                self.service.forms()
                .batchUpdate(body={"requests": requests}, formId=self.id)
                .execute()["replies"]
            )
        except HttpError as e:
            if e.status_code in FATAL_HTTP_CODES:
                raise FatalHttpError(e.resp, e.content, e.uri)
            raise e

    def flush(self, reverse=False):
        if reverse:
            base = reversed(self._change_queue)
        else:
            base = self._change_queue
        final = []
        for item in base:
            if isinstance(item, list):
                for i in item:
                    final.append(i)
            else:
                final.append(item)
        for z in final:
            logger.debug(z)
        if not base:
            return []
        out = self.batch_update(final)
        self._change_queue = []
        self.refresh()
        return out

    @property
    def info(self) -> "Info":
        if self._info_cache:
            return self._info_cache
        item = super().info
        # manually set update mask here
        if isinstance(item._info, WatchedDictionary):
            return item
        uf = lambda: self._mutation(  # noqa: E731
            [UpdateFormInfoRequest(info=item, update_mask="*").wire_format]
        )
        item._info = WatchedDictionary(parent_dict=item._info, update_factory=uf)
        self._info_cache = item
        return item

    @info.setter
    def info(self, item: "Info"):
        uf = lambda: self._mutation(  # noqa: E731
            [UpdateFormInfoRequest(info=item, update_mask="*").wire_format]
        )

        item._info = WatchedDictionary(parent_dict=item._info, update_factory=uf)
        super(Form, self.__class__).info.fset(self, item)  # type: ignore
        self._info_cache = None

    @property
    def settings(self) -> "FormSettings":
        if self._settings_cache:
            return self._settings_cache
        from pygsuite.forms.generated.update_settings_request import UpdateSettingsRequest

        settings = super().settings
        if isinstance(settings._info, WatchedDictionary):
            return settings
        uf = lambda: self._mutation(  # noqa: E731
            [UpdateSettingsRequest(settings=settings).wire_format]
        )
        settings._info = WatchedDictionary(parent_dict=settings._info, update_factory=uf)
        self._settings_cache = settings
        return settings

    @settings.setter
    def settings(self, settings: "FormSettings"):
        from pygsuite.forms.generated.update_settings_request import UpdateSettingsRequest

        uf = lambda: self._mutation(  # noqa: E731
            [UpdateSettingsRequest(settings=settings).wire_format]
        )
        settings._info = WatchedDictionary(parent_dict=settings._info, update_factory=uf)
        super(Form, self.__class__).settings.fset(self, settings)  # type:ignore
        self._settings_cache = None

    @property
    def items(self) -> List["Item"]:
        if self._items_cache:
            return self._items_cache
        base = super().items
        if not isinstance(base, WatchedList):
            base = WatchedList(
                iterable=base,
                update_factory=self.items_update_factory,
                delete_factory=self.items_delete_factory,
                move_factory=self.items_move_factory,
                create_factory=self.items_create_factory,
            )
        self._items_cache = base
        return base

    @items.setter
    def items(self, items: List):
        items = WatchedList(
            iterable=items,
            update_factory=self.items_update_factory,
            delete_factory=self.items_delete_factory,
            move_factory=self.items_move_factory,
            create_factory=self.items_create_factory,
        )
        super(Form, self.__class__).items.fset(self, items)  # type: ignore
        self._items_cache = None

    @retry(HttpError, tries=3, delay=5, backoff=3, fatal_exceptions=(FatalHttpError,))
    def refresh(self):
        self._info = self.service.forms().get(formId=self.id).execute()
        self._info_cache = None
        self._settings_cache = None
        self._items_cache = None

    # def add_item(self, title: str, description: str, item: Union[
    #     "PageBreakItem", "TextItem", "VideoItem", "ImageItem", "QuestionItem", "QuestionGroupItem"],
    #              location: Optional[int] = None, **kwargs):
    #     if not location:
    #         location = len(self.items)
    #     new = {'title': title,
    #            'description': description,
    #            }
    #     new[ItemType(item).value] = item._info
    #     item = Item(info=new, form=self._form, location=location)
    #     # locally modify
    #     self._form['items'].insert(location, new)
    #     # and add synchronization request to queue
    #     self._mutation([CreateItemRequest(item=item, location=location).request])
