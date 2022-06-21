
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class Location(BaseFormItem):
    """
    A specific location in a form.
    """
    def __init__(self, 
                index: Optional[int] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if index:
            generated['index'] =  index 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def index(self)->int:
        return self._info.get('index')
    
    @index.setter
    def index(self, value: int):
        if self._info['index'] == value:
            return
        self._info['index'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

