
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.watch import Watch


class CreateWatchRequest(BaseFormItem):
    """
    Create a new watch.
    """
    def __init__(self, 
                watch: Optional["Watch"] = None,
                watch_id: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if watch:
            generated['watch'] =  watch._info 
        if watch_id:
            generated['watchId'] =  watch_id 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def watch(self)->"Watch":
        return Watch(object_info=self._info.get('watch'))
    
    @watch.setter
    def watch(self, value: "Watch"):
        if self._info['watch'] == value:
            return
        self._info['watch'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def watch_id(self)->str:
        return self._info.get('watchId')
    
    @watch_id.setter
    def watch_id(self, value: str):
        if self._info['watchId'] == value:
            return
        self._info['watchId'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

