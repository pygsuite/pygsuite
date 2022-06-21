
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class TextLink(BaseFormItem):
    """
    Link for text.
    """
    def __init__(self, 
                display_text: Optional[str] = None,
                uri: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if display_text:
            generated['displayText'] =  display_text 
        if uri:
            generated['uri'] =  uri 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def display_text(self)->str:
        return self._info.get('displayText')
    
    @display_text.setter
    def display_text(self, value: str):
        if self._info['displayText'] == value:
            return
        self._info['displayText'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def uri(self)->str:
        return self._info.get('uri')
    
    @uri.setter
    def uri(self, value: str):
        if self._info['uri'] == value:
            return
        self._info['uri'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

