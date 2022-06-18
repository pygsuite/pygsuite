from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygsuite.forms.item import Item


class CreateItemRequest(object):
    def __init__(self, item: "Item", location: int):
        self.item = item
        self.location = location

    @property
    def request(self):
        return {"createItem": {
            "item": self.item._info,
            "location": {'index': self.location},
        }}
