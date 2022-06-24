from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.item import Item
from pygsuite.forms.generated.location import Location


class CreateItemRequest(BaseFormItem):
    """
    Create an item in a form.
    """

    def __init__(
        self,  # noqa: C901
        item: Optional["Item"] = None,
        location: Optional["Location"] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if item is not None:

            generated["item"] = item._info
        if location is not None:

            generated["location"] = location._info
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def item(self) -> "Item":
        return Item(object_info=self._info.get("item"))

    @item.setter
    def item(self, value: "Item"):
        if self._info.get("item", None) == value:
            return
        self._info["item"] = value

    @property
    def location(self) -> "Location":
        return Location(object_info=self._info.get("location"))

    @location.setter
    def location(self, value: "Location"):
        if self._info.get("location", None) == value:
            return
        self._info["location"] = value

    @property
    def wire_format(self) -> dict:
        base = "CreateItem"
        base = base[0].lower() + base[1:]

        return {base: self._info}
