
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
        
        if settings:
            generated['settings'] =  settings._info 
        if update_mask:
            generated['updateMask'] =  update_mask 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def settings(self)->"FormSettings":
        return FormSettings(object_info=self._info.get('settings'))
    
    @settings.setter
    def settings(self, value: "FormSettings"):
        if self._info['settings'] == value:
            return
        self._info['settings'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def update_mask(self)->str:
        return self._info.get('updateMask')
    
    @update_mask.setter
    def update_mask(self, value: str):
        if self._info['updateMask'] == value:
            return
        self._info['updateMask'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

