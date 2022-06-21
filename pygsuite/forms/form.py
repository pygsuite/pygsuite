from typing import Optional, TYPE_CHECKING, Union

from googleapiclient.errors import HttpError

from pygsuite import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.drive.drive_object import DriveObject
from pygsuite.enums import MimeType
from pygsuite.forms.enums import ItemType
from pygsuite.forms.update_requests.create_item import CreateItemRequest
from pygsuite.utility.decorators import retry
from pygsuite.forms.generated.form import Form as BaseForm
from .item import Item

if TYPE_CHECKING:
    from .page_break_item import PageBreakItem
    from .question_item import QuestionItem
    from .question_group_item import QuestionGroupItem
    from .text_item import TextItem
    from .video_item import VideoItem
    from .image_item import ImageItem


class Form( BaseForm, DriveObject):
    """A form on google drive."""

    _mimetype = MimeType.FORMS

    def __init__(self, id: str = None, client=None, name=None, _form=None, local: bool = False):

        if not local:
            client = client or Clients.forms_client
        self.service = client
        self.id = parse_id(id) if id else None
        DriveObject.__init__(self, id=id, client=client)
        BaseForm.__init__(self, object_info = _form or client.forms().get(formId=self.id).execute()  )
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

    @retry(HttpError, tries=3, delay=5, backoff=3)
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
        if not base:
            return []
        print(final)
        out = (
            self.service.forms()
                .batchUpdate(body={"requests": final}, formId=self.id)
                .execute()["replies"]
        )

        self._change_queue = []
        self.refresh()
        return out

    # @property
    # def items(self):
    #     return [Item(item, self, idx) for idx, item in enumerate(self._form.get('items', []))]

    # def delete(self, start=0, end=None, flush=True):
    #     end = end or self.body.end_index
    #     self._mutation([{'deleteContentRange': {'range': {
    #         "segmentId": None,
    #         "startIndex": start,
    #         "endIndex": end
    #     }}}])
    #     if flush:
    #         self.flush()

    def refresh(self):
        self._form = self.service.forms().get(formId=self.id).execute()

    @property
    def url(self):
        return f"https://drive.google.com/forms/d/{self.id}"

    def add_item(self, title: str, description: str, item: Union[
        "PageBreakItem", "TextItem", "VideoItem", "ImageItem", "QuestionItem", "QuestionGroupItem"],
                 location: Optional[int] = None, **kwargs):
        if not location:
            location = len(self.items)
        new = {'title': title,
               'description': description,
               }
        new[ItemType(item).value] = item._info
        item = Item(info=new, form=self._form, location=location)
        # locally modify
        self._form['items'].insert(location, new)
        # and add synchronization request to queue
        self._mutation([CreateItemRequest(item=item, location=location).request])

    # def add_item(self,  title:str, description:str, item_type:ItemType, location:Optional[int] = None, **kwargs):
    #     if not location:
    #         location = len(self.items)
    #     new = {'title': title,
    #            'description':description,
    #            }
    #     enriched = {}
    #
    #     if item_type == ItemType.TEXT_ITEM:
    #         pass
    #     elif item_type == ItemType.IMAGE_ITEM:
    #         enriched['']
    #     elif item_type == ItemType.QUESTION_ITEM:
    #
    #     new[item_type.value] = enriched
    #     item = Item(info=new, form=self._form, location=location)
    #     # locally modify
    #     self._form['items'].insert(new, index=location)
    #     # and add synchronization request to queue
    #     self._mutation([CreateItemRequest(item=item, location=location).request])
    #
