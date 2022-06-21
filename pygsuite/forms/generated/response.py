
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.create_item_response import CreateItemResponse


class Response(BaseFormItem):
    """
    A single response from an update.
    """
    def __init__(self, 
                create_item: Optional["CreateItemResponse"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if create_item is not None:
            generated['createItem'] =  create_item._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def create_item(self)->"CreateItemResponse":
        return CreateItemResponse(object_info=self._info.get('createItem'))
    
    @create_item.setter
    def create_item(self, value: "CreateItemResponse"):
        if self._info.get('createItem',None) == value:
            return
        self._info['createItem'] = value
        
    
    
    
