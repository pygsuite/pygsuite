from typing import Optional, Dict, List

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.extra_material import ExtraMaterial


class Feedback(BaseFormItem):
    """
    Feedback for a respondent about their response to a question.
    """

    def __init__(
        self,
        material: Optional[List["ExtraMaterial"]] = None,
        text: Optional[str] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if material is not None:
            generated["material"] = [v._info for v in material]
        if text is not None:

            generated["text"] = text
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def material(self) -> List["ExtraMaterial"]:
        return [ExtraMaterial(object_info=v) for v in self._info.get("material")]

    @material.setter
    def material(self, value: List["ExtraMaterial"]):
        if self._info.get("material", None) == value:
            return
        self._info["material"] = value

    @property
    def text(self) -> str:
        return self._info.get("text")

    @text.setter
    def text(self, value: str):
        if self._info.get("text", None) == value:
            return
        self._info["text"] = value
