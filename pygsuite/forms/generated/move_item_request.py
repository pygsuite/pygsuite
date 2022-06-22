
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.location import Location
from pygsuite.forms.generated.location import Location


class MoveItemRequest(BaseFormItem):
    """
    Move an item in a form.
    """
    def __init__(self, 
                new_location: Optional["Location"] = None,
                original_location: Optional["Location"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if new_location is not None:
            generated['newLocation'] =  new_location._info 
        if original_location is not None:
            generated['originalLocation'] =  original_location._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def new_location(self)->"Location":
        return Location(object_info=self._info.get('newLocation'))
    
    @new_location.setter
    def new_location(self, value: "Location"):
        if self._info.get('newLocation',None) == value:
            return
        self._info['newLocation'] = value
        
    
    @property
    def original_location(self)->"Location":
        return Location(object_info=self._info.get('originalLocation'))
    
    @original_location.setter
    def original_location(self, value: "Location"):
        if self._info.get('originalLocation',None) == value:
            return
        self._info['originalLocation'] = value
        
    
    
    
    @property
    def wire_format(self)->dict:
        base = 'MoveItem'
        base = base[0].lower() + base[1:]
        request = self._info
        components = 'move_item_request'.split('_')
        # if it's an update, we *may* need to provide an update mask
        # generate this automatically to include all fields
        # can be optionally overridden when creating synchronization method
        if components[0] == 'update':
            if not self.update_mask:
                target_field = [field for field in request.keys() if field not in ['update_mask', 'location']][0]           
                self._info['updateMask'] = ','.join(request[target_field].keys())
        return {base:self._info}
    
