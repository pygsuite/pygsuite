
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class RowQuestion(BaseFormItem):
    """
    Configuration for a question that is part of a question group.
    """
    def __init__(self, 
                title: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if title:
            generated['title'] =  title 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def title(self)->str:
        return self._info.get('title')
    
    @title.setter
    def title(self, value: str):
        if self._info['title'] == value:
            return
        self._info['title'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

