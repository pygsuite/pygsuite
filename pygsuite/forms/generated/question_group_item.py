from typing import Optional, Dict, List

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.grid import Grid
from pygsuite.forms.generated.image import Image
from pygsuite.forms.generated.question import Question


class QuestionGroupItem(BaseFormItem):
    """
    Defines a question that comprises multiple questions grouped together.
    """

    def __init__(
        self,  # noqa: C901
        grid: Optional["Grid"] = None,
        image: Optional["Image"] = None,
        questions: Optional[List["Question"]] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if grid is not None:

            generated["grid"] = grid._info
        if image is not None:

            generated["image"] = image._info
        if questions is not None:
            generated["questions"] = [v._info for v in questions]
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def grid(self) -> "Grid":
        return Grid(object_info=self._info.get("grid"))

    @grid.setter
    def grid(self, value: "Grid"):
        if self._info.get("grid", None) == value:
            return
        self._info["grid"] = value

    @property
    def image(self) -> "Image":
        return Image(object_info=self._info.get("image"))

    @image.setter
    def image(self, value: "Image"):
        if self._info.get("image", None) == value:
            return
        self._info["image"] = value

    @property
    def questions(self) -> List["Question"]:
        return [Question(object_info=v) for v in self._info.get("questions", [])]

    @questions.setter
    def questions(self, value: List["Question"]):
        if self._info.get("questions", None) == value:
            return
        self._info["questions"] = value
