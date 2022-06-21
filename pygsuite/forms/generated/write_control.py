
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class WriteControl(BaseFormItem):
    """
    Provides control over how write requests are executed.
    """
    def __init__(self, 
                required_revision_id: Optional[str] = None,
                target_revision_id: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if required_revision_id:
            generated['requiredRevisionId'] =  required_revision_id 
        if target_revision_id:
            generated['targetRevisionId'] =  target_revision_id 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def required_revision_id(self)->str:
        return self._info.get('requiredRevisionId')
    
    @required_revision_id.setter
    def required_revision_id(self, value: str):
        if self._info['requiredRevisionId'] == value:
            return
        self._info['requiredRevisionId'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def target_revision_id(self)->str:
        return self._info.get('targetRevisionId')
    
    @target_revision_id.setter
    def target_revision_id(self, value: str):
        if self._info['targetRevisionId'] == value:
            return
        self._info['targetRevisionId'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

