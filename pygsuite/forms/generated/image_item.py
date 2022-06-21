
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.image import Image


class ImageItem(BaseFormItem):
    """
    An item containing an image.
    """
    def __init__(self, 
                image: Optional["Image"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if image:
            generated['image'] =  image._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def image(self)->"Image":
        return Image(object_info=self._info.get('image'))
    
    @image.setter
    def image(self, value: "Image"):
        if self._info['image'] == value:
            return
        self._info['image'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

