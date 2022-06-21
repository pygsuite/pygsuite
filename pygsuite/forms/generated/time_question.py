
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class TimeQuestion(BaseFormItem):
    """
    A time question.
    """
    def __init__(self, 
                duration: Optional[bool] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if duration:
            generated['duration'] =  duration 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def duration(self)->bool:
        return self._info.get('duration')
    
    @duration.setter
    def duration(self, value: bool):
        if self._info['duration'] == value:
            return
        self._info['duration'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

