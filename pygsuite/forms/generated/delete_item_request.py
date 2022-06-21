
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.location import Location


class DeleteItemRequest(BaseFormItem):
    """
    Delete an item in a form.
    """
    def __init__(self, 
                location: Optional["Location"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if location is not None:
            generated['location'] =  location._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def location(self)->"Location":
        return Location(object_info=self._info.get('location'))
    
    @location.setter
    def location(self, value: "Location"):
        if self._info.get('location',None) == value:
            return
        self._info['location'] = value
        
    
    
    
    @property
    def wire_format(self)->dict:
        base = 'DeleteItem'
        base = base[0].lower() + base[1:]
        request = self._info
        components = 'delete_item_request'.split('_')
        # if it's an update, we need to provide an update mask
        # generate this automatically to cinlude all fields
        if components[0] == 'update':
            if not self.update_mask:
                target_field = [field for field in request.keys() if field not in ['update_mask', 'location']][0]           
                self._info['updateMask'] = ','.join(request[target_field].keys())
        return {base:self._info}
    
