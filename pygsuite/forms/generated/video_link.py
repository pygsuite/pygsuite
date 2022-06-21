
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class VideoLink(BaseFormItem):
    """
    Link to a video.
    """
    def __init__(self, 
                display_text: Optional[str] = None,
                youtube_uri: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if display_text:
            generated['displayText'] =  display_text 
        if youtube_uri:
            generated['youtubeUri'] =  youtube_uri 
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
    def youtube_uri(self)->str:
        return self._info.get('youtubeUri')
    
    @youtube_uri.setter
    def youtube_uri(self, value: str):
        if self._info['youtubeUri'] == value:
            return
        self._info['youtubeUri'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

