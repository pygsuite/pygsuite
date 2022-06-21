
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.watch import Watch


class ListWatchesResponse(BaseFormItem):
    """
    The response of a ListWatchesRequest.
    """
    def __init__(self, 
                watches: Optional[List["Watch"]] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if watches is not None:
            generated['watches'] =  watches 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def watches(self)->List["Watch"]:
        return [Watch(object_info=v) for v in self._info.get('watches')]
        
    
    @watches.setter
    def watches(self, value: List["Watch"]):
        if self._info.get('watches',None) == value:
            return
        self._info['watches'] = value
        
    
    
    
