from pygsuite.forms.location import Location
from typing import TYPE_CHECKING

from typing import Union

if TYPE_CHECKING:
    from pygsuite.forms.item import Item

class UpdateItemRequest(object):
    def __init__(self, item:"Item", location:int):
        self.item = item
        self.location = location

    @property
    def request(self):
        return {"updateItem":{
            "item": self.item._info,
            "location": {'index':self.location},
            "updateMask": ','.join([key for key in self.item._info.keys()])
        }}