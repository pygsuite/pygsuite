
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class ScaleQuestion(BaseFormItem):
    """
    A scale question. The user has a range of numeric values to choose from.
    """
    def __init__(self, 
                high: Optional[int] = None,
                high_label: Optional[str] = None,
                low: Optional[int] = None,
                low_label: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if high:
            generated['high'] =  high 
        if high_label:
            generated['highLabel'] =  high_label 
        if low:
            generated['low'] =  low 
        if low_label:
            generated['lowLabel'] =  low_label 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def high(self)->int:
        return self._info.get('high')
    
    @high.setter
    def high(self, value: int):
        if self._info['high'] == value:
            return
        self._info['high'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def high_label(self)->str:
        return self._info.get('highLabel')
    
    @high_label.setter
    def high_label(self, value: str):
        if self._info['highLabel'] == value:
            return
        self._info['highLabel'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def low(self)->int:
        return self._info.get('low')
    
    @low.setter
    def low(self, value: int):
        if self._info['low'] == value:
            return
        self._info['low'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def low_label(self)->str:
        return self._info.get('lowLabel')
    
    @low_label.setter
    def low_label(self, value: str):
        if self._info['lowLabel'] == value:
            return
        self._info['lowLabel'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

