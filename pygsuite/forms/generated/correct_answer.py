
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class CorrectAnswer(BaseFormItem):
    """
    A single correct answer for a question. For multiple-valued (`CHECKBOX`) questions, several `CorrectAnswer`s may be needed to represent a single correct response option.
    """
    def __init__(self, 
                value: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if value:
            generated['value'] =  value 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def value(self)->str:
        return self._info.get('value')
    
    @value.setter
    def value(self, value: str):
        if self._info['value'] == value:
            return
        self._info['value'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

