from typing import Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.image import Image
from pygsuite.forms.generated.question import Question


class QuestionItem(BaseFormItem):
    """
    A form item containing a single question.
    """

    def __init__(
        self,
        image: Optional["Image"] = None,
        question: Optional["Question"] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if image is not None:

            generated["image"] = image._info
        if question is not None:

            generated["question"] = question._info
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def image(self) -> "Image":
        return Image(object_info=self._info.get("image"))

    @image.setter
    def image(self, value: "Image"):
        if self._info.get("image", None) == value:
            return
        self._info["image"] = value

    @property
    def question(self) -> "Question":
        return Question(object_info=self._info.get("question"))

    @question.setter
    def question(self, value: "Question"):
        if self._info.get("question", None) == value:
            return
        self._info["question"] = value
