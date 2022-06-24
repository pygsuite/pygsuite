from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem


class TextQuestion(BaseFormItem):
    """
    A text-based question.
    """

    def __init__(  # noqa: C901
        self, paragraph: Optional[bool] = None, object_info: Optional[Dict] = None
    ):
        generated: Dict = {}

        if paragraph is not None:

            generated["paragraph"] = paragraph
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def paragraph(self) -> bool:
        return self._info.get("paragraph")

    @paragraph.setter
    def paragraph(self, value: bool):
        if self._info.get("paragraph", None) == value:
            return
        self._info["paragraph"] = value
