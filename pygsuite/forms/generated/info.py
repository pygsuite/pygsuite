
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class Info(BaseFormItem):
    """
    The general information for a form.
    """
    def __init__(self, 
                description: Optional[str] = None,
                title: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if description:
            generated['description'] =  description 
        if title:
            generated['title'] =  title 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def description(self)->str:
        return self._info.get('description')
    
    @description.setter
    def description(self, value: str):
        if self._info['description'] == value:
            return
        self._info['description'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def document_title(self)->str:
        return self._info.get('documentTitle')
    
    @property
    def title(self)->str:
        return self._info.get('title')
    
    @title.setter
    def title(self, value: str):
        if self._info['title'] == value:
            return
        self._info['title'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

