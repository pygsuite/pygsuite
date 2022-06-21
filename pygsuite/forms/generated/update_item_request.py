
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
        
        if item is not None:
            generated['item'] =  item._info 
        if location is not None:
            generated['location'] =  location._info 
        if update_mask is not None:
            generated['updateMask'] =  update_mask 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def item(self)->"Item":
        return Item(object_info=self._info.get('item'))
    
    @item.setter
    def item(self, value: "Item"):
        if self._info.get('item',None) == value:
            return
        self._info['item'] = value
        
    
    @property
    def location(self)->"Location":
        return Location(object_info=self._info.get('location'))
    
    @location.setter
    def location(self, value: "Location"):
        if self._info.get('location',None) == value:
            return
        self._info['location'] = value
        
    
    @property
    def update_mask(self)->str:
        return self._info.get('updateMask')
    
    @update_mask.setter
    def update_mask(self, value: str):
        if self._info.get('updateMask',None) == value:
            return
        self._info['updateMask'] = value
        
    
    
    
    @property
    def wire_format(self)->dict:
        base = 'UpdateItem'
        base = base[0].lower() + base[1:]
        request = self._info
        components = 'update_item_request'.split('_')
        # if it's an update, we need to provide an update mask
        # generate this automatically to cinlude all fields
        if components[0] == 'update':
            if not self.update_mask:
                target_field = [field for field in request.keys() if field not in ['update_mask', 'location']][0]           
                self._info['updateMask'] = ','.join(request[target_field].keys())
        return {base:self._info}
    
