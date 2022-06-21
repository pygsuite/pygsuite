
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class CreateItemResponse(BaseFormItem):
    """
    The result of creating an item.
    """
    def __init__(self, 
                item_id: Optional[str] = None,
                question_id: Optional[List["str"]] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if item_id is not None:
            generated['itemId'] =  item_id 
        if question_id is not None:
            generated['questionId'] =  question_id 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def item_id(self)->str:
        return self._info.get('itemId')
    
    @item_id.setter
    def item_id(self, value: str):
        if self._info.get('itemId',None) == value:
            return
        self._info['itemId'] = value
        
    
    @property
    def question_id(self)->List["str"]:
        return [v for v in self._info.get('questionId')]
        
    
    @question_id.setter
    def question_id(self, value: List["str"]):
        if self._info.get('questionId',None) == value:
            return
        self._info['questionId'] = value
        
    
    
    
