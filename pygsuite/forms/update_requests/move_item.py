from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygsuite.forms.item import Item


class MoveItemRequest(object):
    def __init__(self, original_location:int , new_location:int):
        self.original_location = original_location
        self.new_location = new_location

    @property
    def request(self):
        return {"moveItem": {
            "originalLocation": {'index': self.original_location},
            "newLocation": {'index': self.new_location},
        }}
