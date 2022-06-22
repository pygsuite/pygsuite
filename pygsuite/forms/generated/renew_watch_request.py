
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class RenewWatchRequest(BaseFormItem):
    """
    Renew an existing Watch for seven days.
    """
    def __init__(self, 
                object_info: Optional[Dict] = None):
        generated = {}
        
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    
    
    @property
    def wire_format(self)->dict:
        base = 'RenewWatch'
        base = base[0].lower() + base[1:]
        request = self._info
        components = 'renew_watch_request'.split('_')
        # if it's an update, we *may* need to provide an update mask
        # generate this automatically to include all fields
        # can be optionally overridden when creating synchronization method
        if components[0] == 'update':
            if not self.update_mask:
                target_field = [field for field in request.keys() if field not in ['update_mask', 'location']][0]           
                self._info['updateMask'] = ','.join(request[target_field].keys())
        return {base:self._info}
    
