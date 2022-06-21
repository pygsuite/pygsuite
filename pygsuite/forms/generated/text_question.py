
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class TextQuestion(BaseFormItem):
    """
    A text-based question.
    """
    def __init__(self, 
                paragraph: Optional[bool] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if paragraph:
            generated['paragraph'] =  paragraph 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def paragraph(self)->bool:
        return self._info.get('paragraph')
    
    @paragraph.setter
    def paragraph(self, value: bool):
        if self._info['paragraph'] == value:
            return
        self._info['paragraph'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

