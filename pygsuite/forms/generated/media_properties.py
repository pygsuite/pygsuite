
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class MediaProperties(BaseFormItem):
    """
    Properties of the media.
    """
    def __init__(self, 
                alignment: Optional[str] = None,
                width: Optional[int] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if alignment:
            generated['alignment'] =  alignment 
        if width:
            generated['width'] =  width 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def alignment(self)->str:
        return self._info.get('alignment')
    
    @alignment.setter
    def alignment(self, value: str):
        if self._info['alignment'] == value:
            return
        self._info['alignment'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def width(self)->int:
        return self._info.get('width')
    
    @width.setter
    def width(self, value: int):
        if self._info['width'] == value:
            return
        self._info['width'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

