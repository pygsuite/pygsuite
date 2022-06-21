
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.info import Info


class UpdateFormInfoRequest(BaseFormItem):
    """
    Update Form's Info.
    """
    def __init__(self, 
                info: Optional["Info"] = None,
                update_mask: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if info:
            generated['info'] =  info._info 
        if update_mask:
            generated['updateMask'] =  update_mask 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def info(self)->"Info":
        return Info(object_info=self._info.get('info'))
    
    @info.setter
    def info(self, value: "Info"):
        if self._info['info'] == value:
            return
        self._info['info'] = value
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
    

