
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.media_properties import MediaProperties


class Image(BaseFormItem):
    """
    Data representing an image.
    """
    def __init__(self, 
                alt_text: Optional[str] = None,
                properties: Optional["MediaProperties"] = None,
                source_uri: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if alt_text:
            generated['altText'] =  alt_text 
        if properties:
            generated['properties'] =  properties._info 
        if source_uri:
            generated['sourceUri'] =  source_uri 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def alt_text(self)->str:
        return self._info.get('altText')
    
    @alt_text.setter
    def alt_text(self, value: str):
        if self._info['altText'] == value:
            return
        self._info['altText'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def content_uri(self)->str:
        return self._info.get('contentUri')
    
    @property
    def properties(self)->"MediaProperties":
        return MediaProperties(object_info=self._info.get('properties'))
    
    @properties.setter
    def properties(self, value: "MediaProperties"):
        if self._info['properties'] == value:
            return
        self._info['properties'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def source_uri(self)->str:
        return self._info.get('sourceUri')
    
    @source_uri.setter
    def source_uri(self, value: str):
        if self._info['sourceUri'] == value:
            return
        self._info['sourceUri'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

