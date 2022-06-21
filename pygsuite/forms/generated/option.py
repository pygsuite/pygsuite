
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.image import Image


class Option(BaseFormItem):
    """
    An option for a Choice question.
    """
    def __init__(self, 
                go_to_action: Optional[str] = None,
                go_to_section_id: Optional[str] = None,
                image: Optional["Image"] = None,
                is_other: Optional[bool] = None,
                value: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if go_to_action:
            generated['goToAction'] =  go_to_action 
        if go_to_section_id:
            generated['goToSectionId'] =  go_to_section_id 
        if image:
            generated['image'] =  image._info 
        if is_other:
            generated['isOther'] =  is_other 
        if value:
            generated['value'] =  value 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def go_to_action(self)->str:
        return self._info.get('goToAction')
    
    @go_to_action.setter
    def go_to_action(self, value: str):
        if self._info['goToAction'] == value:
            return
        self._info['goToAction'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def go_to_section_id(self)->str:
        return self._info.get('goToSectionId')
    
    @go_to_section_id.setter
    def go_to_section_id(self, value: str):
        if self._info['goToSectionId'] == value:
            return
        self._info['goToSectionId'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def image(self)->"Image":
        return Image(object_info=self._info.get('image'))
    
    @image.setter
    def image(self, value: "Image"):
        if self._info['image'] == value:
            return
        self._info['image'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def is_other(self)->bool:
        return self._info.get('isOther')
    
    @is_other.setter
    def is_other(self, value: bool):
        if self._info['isOther'] == value:
            return
        self._info['isOther'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def value(self)->str:
        return self._info.get('value')
    
    @value.setter
    def value(self, value: str):
        if self._info['value'] == value:
            return
        self._info['value'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

