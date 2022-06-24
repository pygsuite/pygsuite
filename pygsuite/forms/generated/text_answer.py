from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem


class TextAnswer(BaseFormItem):
    """
    An answer to a question represented as text.
    """

    def __init__(self, object_info: Optional[Dict] = None):  # noqa: C901
        generated: Dict = {}

        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def value(self) -> str:
        return self._info.get("value")
