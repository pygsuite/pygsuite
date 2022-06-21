
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.info import Info
from pygsuite.forms.generated.item import Item
from pygsuite.forms.generated.form_settings import FormSettings


class Form(BaseFormItem):
    """
    A Google Forms document. A form is created in Drive, and deleting a form or changing its access protections is done via the [Drive API](https://developers.google.com/drive/api/v3/about-sdk).
    """
    def __init__(self, 
                info: Optional["Info"] = None,
                items: Optional[List["Item"]] = None,
                settings: Optional["FormSettings"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if info is not None:
            generated['info'] =  info._info 
        if items is not None:
            generated['items'] =  items 
        if settings is not None:
            generated['settings'] =  settings._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def form_id(self)->str:
        return self._info.get('formId')
    
    @property
    def info(self)->"Info":
        return Info(object_info=self._info.get('info'))
    
    @info.setter
    def info(self, value: "Info"):
        if self._info.get('info',None) == value:
            return
        self._info['info'] = value
        
    
    @property
    def items(self)->List["Item"]:
        return [Item(object_info=v) for v in self._info.get('items')]
        
    
    @items.setter
    def items(self, value: List["Item"]):
        if self._info.get('items',None) == value:
            return
        self._info['items'] = value
        
    
    @property
    def linked_sheet_id(self)->str:
        return self._info.get('linkedSheetId')
    
    @property
    def responder_uri(self)->str:
        return self._info.get('responderUri')
    
    @property
    def revision_id(self)->str:
        return self._info.get('revisionId')
    
    @property
    def settings(self)->"FormSettings":
        return FormSettings(object_info=self._info.get('settings'))
    
    @settings.setter
    def settings(self, value: "FormSettings"):
        if self._info.get('settings',None) == value:
            return
        self._info['settings'] = value
        
    
    
    
