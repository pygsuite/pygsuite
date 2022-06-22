from typing import TYPE_CHECKING

from googleapiclient.errors import HttpError

from pygsuite import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.constants import FATAL_HTTP_CODES
from pygsuite.constants import logger
from pygsuite.drive.drive_object import DriveObject
from pygsuite.enums import MimeType
from pygsuite.exceptions import FatalHttpError
from pygsuite.forms.generated.form import Form as BaseForm
from pygsuite.forms.synchronizer import WatchedList, WatchedDictionary
from pygsuite.utility.decorators import retry

if TYPE_CHECKING:
    from .generated.form_settings import FormSettings
    from .generated.info import Info


class Form(BaseForm, DriveObject):
    """A form on google drive."""

    _mimetype = MimeType.FORMS

    _base_url = "https://docs.google.com/forms/d/{}/edit"

    def __init__(self, id: str = None, client=None, name=None, _form=None, local: bool = False):

        if not local:
            client = client or Clients.forms_client
        self.service = client
        self.id = parse_id(id) if id else None
        DriveObject.__init__(self, id=id, client=client)
        BaseForm.__init__(self, object_info=_form or client.forms().get(formId=self.id).execute())
        self._change_queue = []
        self.auto_sync = False

    def id(self):
        return self._form["id"]

    def _mutation(self, reqs, flush: bool = False):
        if not reqs:
            return None
        self._change_queue += reqs
        if flush or self.auto_sync:
            return self.flush()

    @retry(HttpError, tries=3, delay=5, backoff=3, fatal_exceptions=(FatalHttpError,))
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
        try:
            out = (
                self.service.forms()
                .batchUpdate(body={"requests": final}, formId=self.id)
                .execute()["replies"]
            )
        except HttpError as e:
            if e.status_code in FATAL_HTTP_CODES:
                raise FatalHttpError(e.resp, e.content, e.uri)
            raise e
        self._change_queue = []
        self.refresh()
        return out

    @property
    def info(self) -> "Info":
        from pygsuite.forms.generated.update_form_info_request import UpdateFormInfoRequest
        from pygsuite.forms.synchronizer import WatchedDictionary

        item = super().info
        # manually set update mask here
        uf = lambda: self._mutation([UpdateFormInfoRequest(info=item, update_mask="*").wire_format])
        item._info = WatchedDictionary(parent_dict=item._info, update_factory=uf)
        return item

    @property
    def settings(self) -> "FormSettings":
        from pygsuite.forms.generated.update_settings_request import UpdateSettingsRequest

        settings = super().settings
        uf = lambda: self._mutation([UpdateSettingsRequest(settings=settings).wire_format])
        settings._info = WatchedDictionary(parent_dict=settings._info, update_factory=uf)
        return settings

    @property
    def items(self) -> WatchedList["Item"]:
        from pygsuite.forms.generated.update_item_request import UpdateItemRequest
        from pygsuite.forms.generated.delete_item_request import DeleteItemRequest
        from pygsuite.forms.generated.move_item_request import MoveItemRequest
        from pygsuite.forms.generated.create_item_request import CreateItemRequest
        from pygsuite.forms.generated.location import Location

        def update_factory(idx, item):
            self._mutation([UpdateItemRequest(item=item, location=Location(index=idx)).wire_format])

        def delete_factory(idx):
            self._mutation([DeleteItemRequest(location=Location(index=idx)).wire_format])

        def move_factory(original_idx, new_idx):
            self._mutation(
                [
                    MoveItemRequest(
                        new_location=Location(new_idx), original_location=Location(original_idx)
                    ).wire_format
                ]
            )

        def create_factory(item, idx):
            self._mutation([CreateItemRequest(item, location=Location(idx)).wire_format])

        base = super().items
        return WatchedList(
            iterable=base,
            update_factory=update_factory,
            delete_factory=delete_factory,
            move_factory=move_factory,
            create_factory=create_factory,
        )

    @retry(HttpError, tries=3, delay=5, backoff=3, fatal_exceptions=(FatalHttpError,))
    def refresh(self):
        self._form = self.service.forms().get(formId=self.id).execute()

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
