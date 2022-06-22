from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.image_item import ImageItem
from pygsuite.forms.generated.page_break_item import PageBreakItem
from pygsuite.forms.generated.question_group_item import QuestionGroupItem
from pygsuite.forms.generated.question_item import QuestionItem
from pygsuite.forms.generated.text_item import TextItem
from pygsuite.forms.generated.video_item import VideoItem


class Item(BaseFormItem):
    """
    A single item of the form. `kind` defines which kind of item it is.
    """

    def __init__(  # noqa: C901
        self,
        description: Optional[str] = None,
        image_item: Optional["ImageItem"] = None,
        item_id: Optional[str] = None,
        page_break_item: Optional["PageBreakItem"] = None,
        question_group_item: Optional["QuestionGroupItem"] = None,
        question_item: Optional["QuestionItem"] = None,
        text_item: Optional["TextItem"] = None,
        title: Optional[str] = None,
        video_item: Optional["VideoItem"] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if description is not None:
            generated["description"] = description
        if image_item is not None:
            generated["imageItem"] = image_item._info
        if item_id is not None:
            generated["itemId"] = item_id
        if page_break_item is not None:
            generated["pageBreakItem"] = page_break_item._info
        if question_group_item is not None:
            generated["questionGroupItem"] = question_group_item._info
        if question_item is not None:
            generated["questionItem"] = question_item._info
        if text_item is not None:
            generated["textItem"] = text_item._info
        if title is not None:
            generated["title"] = title
        if video_item is not None:
            generated["videoItem"] = video_item._info
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def description(self) -> str:
        return self._info.get("description")

    @description.setter
    def description(self, value: str):
        if self._info.get("description", None) == value:
            return
        self._info["description"] = value

    @property
    def image_item(self) -> "ImageItem":
        return ImageItem(object_info=self._info.get("imageItem"))

    @image_item.setter
    def image_item(self, value: "ImageItem"):
        if self._info.get("imageItem", None) == value:
            return
        self._info["imageItem"] = value

    @property
    def item_id(self) -> str:
        return self._info.get("itemId")

    @item_id.setter
    def item_id(self, value: str):
        if self._info.get("itemId", None) == value:
            return
        self._info["itemId"] = value

    @property
    def page_break_item(self) -> "PageBreakItem":
        return PageBreakItem(object_info=self._info.get("pageBreakItem"))

    @page_break_item.setter
    def page_break_item(self, value: "PageBreakItem"):
        if self._info.get("pageBreakItem", None) == value:
            return
        self._info["pageBreakItem"] = value

    @property
    def question_group_item(self) -> "QuestionGroupItem":
        return QuestionGroupItem(object_info=self._info.get("questionGroupItem"))

    @question_group_item.setter
    def question_group_item(self, value: "QuestionGroupItem"):
        if self._info.get("questionGroupItem", None) == value:
            return
        self._info["questionGroupItem"] = value

    @property
    def question_item(self) -> "QuestionItem":
        return QuestionItem(object_info=self._info.get("questionItem"))

    @question_item.setter
    def question_item(self, value: "QuestionItem"):
        if self._info.get("questionItem", None) == value:
            return
        self._info["questionItem"] = value

    @property
    def text_item(self) -> "TextItem":
        return TextItem(object_info=self._info.get("textItem"))

    @text_item.setter
    def text_item(self, value: "TextItem"):
        if self._info.get("textItem", None) == value:
            return
        self._info["textItem"] = value

    @property
    def title(self) -> str:
        return self._info.get("title")

    @title.setter
    def title(self, value: str):
        if self._info.get("title", None) == value:
            return
        self._info["title"] = value

    @property
    def video_item(self) -> "VideoItem":
        return VideoItem(object_info=self._info.get("videoItem"))

    @video_item.setter
    def video_item(self, value: "VideoItem"):
        if self._info.get("videoItem", None) == value:
            return
        self._info["videoItem"] = value
