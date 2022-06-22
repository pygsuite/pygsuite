
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.form_settings import FormSettings


class UpdateSettingsRequest(BaseFormItem):
    """
    Update Form's FormSettings.
    """
    def __init__(self, 
                settings: Optional["FormSettings"] = None,
                update_mask: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if settings is not None:
            generated['settings'] =  settings._info 
        if update_mask is not None:
            generated['updateMask'] =  update_mask 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def settings(self)->"FormSettings":
        return FormSettings(object_info=self._info.get('settings'))
    
    @settings.setter
    def settings(self, value: "FormSettings"):
        if self._info.get('settings',None) == value:
            return
        self._info['settings'] = value
        
    
    @property
    def update_mask(self)->str:
        return self._info.get('updateMask')
    
    @update_mask.setter
    def update_mask(self, value: str):
        if self._info.get('updateMask',None) == value:
            return
        self._info['updateMask'] = value
        
    
    
    
    @property
    def wire_format(self)->dict:
        base = 'UpdateSettings'
        base = base[0].lower() + base[1:]
        request = self._info
        components = 'update_settings_request'.split('_')
        # if it's an update, we *may* need to provide an update mask
        # generate this automatically to include all fields
        # can be optionally overridden when creating synchronization method
        if components[0] == 'update':
            if not self.update_mask:
                target_field = [field for field in request.keys() if field not in ['update_mask', 'location']][0]           
                self._info['updateMask'] = ','.join(request[target_field].keys())
        return {base:self._info}
    
