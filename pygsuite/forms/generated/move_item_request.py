
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
        
        if new_location:
            generated['newLocation'] =  new_location._info 
        if original_location:
            generated['originalLocation'] =  original_location._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def new_location(self)->"Location":
        return Location(object_info=self._info.get('newLocation'))
    
    @new_location.setter
    def new_location(self, value: "Location"):
        if self._info['newLocation'] == value:
            return
        self._info['newLocation'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def original_location(self)->"Location":
        return Location(object_info=self._info.get('originalLocation'))
    
    @original_location.setter
    def original_location(self, value: "Location"):
        if self._info['originalLocation'] == value:
            return
        self._info['originalLocation'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

