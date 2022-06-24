from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem


class TextLink(BaseFormItem):
    """
    Link for text.
    """

    def __init__(  # noqa: C901
        self,
        display_text: Optional[str] = None,
        uri: Optional[str] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if display_text is not None:

            generated["displayText"] = display_text
        if uri is not None:

            generated["uri"] = uri
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def display_text(self) -> str:
        return self._info.get("displayText")

    @display_text.setter
    def display_text(self, value: str):
        if self._info.get("displayText", None) == value:
            return
        self._info["displayText"] = value

    @property
    def uri(self) -> str:
        return self._info.get("uri")

    @uri.setter
    def uri(self, value: str):
        if self._info.get("uri", None) == value:
            return
        self._info["uri"] = value
