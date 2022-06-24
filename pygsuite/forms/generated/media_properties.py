from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem


class MediaProperties(BaseFormItem):
    """
    Properties of the media.
    """

    def __init__(
        self,  # noqa: C901
        alignment: Optional[str] = None,
        width: Optional[int] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if alignment is not None:

            generated["alignment"] = alignment
        if width is not None:

            generated["width"] = width
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def alignment(self) -> str:
        return self._info.get("alignment")

    @alignment.setter
    def alignment(self, value: str):
        if self._info.get("alignment", None) == value:
            return
        self._info["alignment"] = value

    @property
    def width(self) -> int:
        return self._info.get("width")

    @width.setter
    def width(self, value: int):
        if self._info.get("width", None) == value:
            return
        self._info["width"] = value
