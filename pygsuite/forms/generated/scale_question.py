
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
        
        if high is not None:
            generated['high'] =  high 
        if high_label is not None:
            generated['highLabel'] =  high_label 
        if low is not None:
            generated['low'] =  low 
        if low_label is not None:
            generated['lowLabel'] =  low_label 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def high(self)->int:
        return self._info.get('high')
    
    @high.setter
    def high(self, value: int):
        if self._info.get('high',None) == value:
            return
        self._info['high'] = value
        
    
    @property
    def high_label(self)->str:
        return self._info.get('highLabel')
    
    @high_label.setter
    def high_label(self, value: str):
        if self._info.get('highLabel',None) == value:
            return
        self._info['highLabel'] = value
        
    
    @property
    def low(self)->int:
        return self._info.get('low')
    
    @low.setter
    def low(self, value: int):
        if self._info.get('low',None) == value:
            return
        self._info['low'] = value
        
    
    @property
    def low_label(self)->str:
        return self._info.get('lowLabel')
    
    @low_label.setter
    def low_label(self, value: str):
        if self._info.get('lowLabel',None) == value:
            return
        self._info['lowLabel'] = value
        
    
    
    
