
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
        
        if watch is not None:
            generated['watch'] =  watch._info 
        if watch_id is not None:
            generated['watchId'] =  watch_id 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def watch(self)->"Watch":
        return Watch(object_info=self._info.get('watch'))
    
    @watch.setter
    def watch(self, value: "Watch"):
        if self._info.get('watch',None) == value:
            return
        self._info['watch'] = value
        
    
    @property
    def watch_id(self)->str:
        return self._info.get('watchId')
    
    @watch_id.setter
    def watch_id(self, value: str):
        if self._info.get('watchId',None) == value:
            return
        self._info['watchId'] = value
        
    
    
    
    @property
    def wire_format(self)->dict:
        base = 'CreateWatch'
        base = base[0].lower() + base[1:]
        request = self._info
        components = 'create_watch_request'.split('_')
        # if it's an update, we need to provide an update mask
        # generate this automatically to cinlude all fields
        if components[0] == 'update':
            if not self.update_mask:
                target_field = [field for field in request.keys() if field not in ['update_mask', 'location']][0]           
                self._info['updateMask'] = ','.join(request[target_field].keys())
        return {base:self._info}
    
