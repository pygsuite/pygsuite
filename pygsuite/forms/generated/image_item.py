from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.image import Image


class ImageItem(BaseFormItem):
    """
    An item containing an image.
    """

    def __init__(
        self, image: Optional["Image"] = None, object_info: Optional[Dict] = None  # noqa: C901
    ):
        generated: Dict = {}

        if image is not None:

            generated["image"] = image._info
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
