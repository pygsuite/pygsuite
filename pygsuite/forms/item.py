from typing import TYPE_CHECKING, Optional

from .base_object import BaseFormItem
from .image_item import ImageItem
from .page_break_item import PageBreakItem
from .question_group_item import QuestionGroupItem
from .question_item import QuestionItem
from .text_item import TextItem
from .update_requests.update_item import UpdateItemRequest
from .video_item import VideoItem
from .enums import ItemType

if TYPE_CHECKING:
    from pygsuite.forms.form import Form


class Item(BaseFormItem):
    VALID_SUBKEYS = {'questionItem': QuestionItem,
                     'questionGroupItem': QuestionGroupItem,
                     'pageBreakItem': PageBreakItem,
                     'textItem': TextItem,
                     'imageItem': ImageItem,
                     'videoItem': VideoItem}

    def __init__(self, info: dict, form: "Form", location: int):
        super().__init__(info, form)
        self.location = location

    # @classmethod
    # def create(cls, title:str, description:str, item_type:ItemType, location:Optional[int] = None, **kwargs):
    #
    @property
    def item_id(self):
        return self._info.get('itemId')

    @property
    def title(self):
        return self._info.get('title')

    @title.setter
    def title(self, value: str):
        if self._info['title'] == value:
            return
        self._info['title'] = value
        self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])

    @property
    def description(self):
        return self._info.get('description')

    @property
    def content(self):
        for key, value in self.VALID_SUBKEYS.items():
            if self._info.get(key) is not None:
                return value(self._info.get(key), self._form)

    @property
    def kind(self) -> str:
        for key in self.VALID_SUBKEYS.keys():
            if key in self._info:
                return key
        return 'unknown'
