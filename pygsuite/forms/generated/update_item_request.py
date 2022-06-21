
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.item import Item
from pygsuite.forms.generated.location import Location


class UpdateItemRequest(BaseFormItem):
    """
    Update an item in a form.
    """
    def __init__(self, 
                item: Optional["Item"] = None,
                location: Optional["Location"] = None,
                update_mask: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if item:
            generated['item'] =  item._info 
        if location:
            generated['location'] =  location._info 
        if update_mask:
            generated['updateMask'] =  update_mask 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def item(self)->"Item":
        return Item(object_info=self._info.get('item'))
    
    @item.setter
    def item(self, value: "Item"):
        if self._info['item'] == value:
            return
        self._info['item'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def location(self)->"Location":
        return Location(object_info=self._info.get('location'))
    
    @location.setter
    def location(self, value: "Location"):
        if self._info['location'] == value:
            return
        self._info['location'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def update_mask(self)->str:
        return self._info.get('updateMask')
    
    @update_mask.setter
    def update_mask(self, value: str):
        if self._info['updateMask'] == value:
            return
        self._info['updateMask'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

