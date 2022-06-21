
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.option import Option


class ChoiceQuestion(BaseFormItem):
    """
    A radio/checkbox/dropdown question.
    """
    def __init__(self, 
                options: Optional[List["Option"]] = None,
                shuffle: Optional[bool] = None,
                type: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if options:
            generated['options'] =  options 
        if shuffle:
            generated['shuffle'] =  shuffle 
        if type:
            generated['type'] =  type 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def options(self)->List["Option"]:
        return [Option(object_info=v) for v in self._info.get('options')]
        
    
    @options.setter
    def options(self, value: List["Option"]):
        if self._info['options'] == value:
            return
        self._info['options'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def shuffle(self)->bool:
        return self._info.get('shuffle')
    
    @shuffle.setter
    def shuffle(self, value: bool):
        if self._info['shuffle'] == value:
            return
        self._info['shuffle'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def type(self)->str:
        return self._info.get('type')
    
    @type.setter
    def type(self, value: str):
        if self._info['type'] == value:
            return
        self._info['type'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

