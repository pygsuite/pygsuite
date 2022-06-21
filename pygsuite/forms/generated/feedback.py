
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.extra_material import ExtraMaterial


class Feedback(BaseFormItem):
    """
    Feedback for a respondent about their response to a question.
    """
    def __init__(self, 
                material: Optional[List["ExtraMaterial"]] = None,
                text: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if material:
            generated['material'] =  material 
        if text:
            generated['text'] =  text 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def material(self)->List["ExtraMaterial"]:
        return [ExtraMaterial(object_info=v) for v in self._info.get('material')]
        
    
    @material.setter
    def material(self, value: List["ExtraMaterial"]):
        if self._info['material'] == value:
            return
        self._info['material'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def text(self)->str:
        return self._info.get('text')
    
    @text.setter
    def text(self, value: str):
        if self._info['text'] == value:
            return
        self._info['text'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

