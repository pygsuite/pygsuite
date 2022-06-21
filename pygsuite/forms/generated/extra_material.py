
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.text_link import TextLink
from pygsuite.forms.generated.video_link import VideoLink


class ExtraMaterial(BaseFormItem):
    """
    Supplementary material to the feedback.
    """
    def __init__(self, 
                link: Optional["TextLink"] = None,
                video: Optional["VideoLink"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if link:
            generated['link'] =  link._info 
        if video:
            generated['video'] =  video._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def link(self)->"TextLink":
        return TextLink(object_info=self._info.get('link'))
    
    @link.setter
    def link(self, value: "TextLink"):
        if self._info['link'] == value:
            return
        self._info['link'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def video(self)->"VideoLink":
        return VideoLink(object_info=self._info.get('video'))
    
    @video.setter
    def video(self, value: "VideoLink"):
        if self._info['video'] == value:
            return
        self._info['video'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

