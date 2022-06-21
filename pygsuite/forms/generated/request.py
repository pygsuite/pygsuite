
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.create_item_request import CreateItemRequest
from pygsuite.forms.generated.delete_item_request import DeleteItemRequest
from pygsuite.forms.generated.move_item_request import MoveItemRequest
from pygsuite.forms.generated.update_form_info_request import UpdateFormInfoRequest
from pygsuite.forms.generated.update_item_request import UpdateItemRequest
from pygsuite.forms.generated.update_settings_request import UpdateSettingsRequest


class Request(BaseFormItem):
    """
    The kinds of update requests that can be made.
    """
    def __init__(self, 
                create_item: Optional["CreateItemRequest"] = None,
                delete_item: Optional["DeleteItemRequest"] = None,
                move_item: Optional["MoveItemRequest"] = None,
                update_form_info: Optional["UpdateFormInfoRequest"] = None,
                update_item: Optional["UpdateItemRequest"] = None,
                update_settings: Optional["UpdateSettingsRequest"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if create_item is not None:
            generated['createItem'] =  create_item._info 
        if delete_item is not None:
            generated['deleteItem'] =  delete_item._info 
        if move_item is not None:
            generated['moveItem'] =  move_item._info 
        if update_form_info is not None:
            generated['updateFormInfo'] =  update_form_info._info 
        if update_item is not None:
            generated['updateItem'] =  update_item._info 
        if update_settings is not None:
            generated['updateSettings'] =  update_settings._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def create_item(self)->"CreateItemRequest":
        return CreateItemRequest(object_info=self._info.get('createItem'))
    
    @create_item.setter
    def create_item(self, value: "CreateItemRequest"):
        if self._info.get('createItem',None) == value:
            return
        self._info['createItem'] = value
        
    
    @property
    def delete_item(self)->"DeleteItemRequest":
        return DeleteItemRequest(object_info=self._info.get('deleteItem'))
    
    @delete_item.setter
    def delete_item(self, value: "DeleteItemRequest"):
        if self._info.get('deleteItem',None) == value:
            return
        self._info['deleteItem'] = value
        
    
    @property
    def move_item(self)->"MoveItemRequest":
        return MoveItemRequest(object_info=self._info.get('moveItem'))
    
    @move_item.setter
    def move_item(self, value: "MoveItemRequest"):
        if self._info.get('moveItem',None) == value:
            return
        self._info['moveItem'] = value
        
    
    @property
    def update_form_info(self)->"UpdateFormInfoRequest":
        return UpdateFormInfoRequest(object_info=self._info.get('updateFormInfo'))
    
    @update_form_info.setter
    def update_form_info(self, value: "UpdateFormInfoRequest"):
        if self._info.get('updateFormInfo',None) == value:
            return
        self._info['updateFormInfo'] = value
        
    
    @property
    def update_item(self)->"UpdateItemRequest":
        return UpdateItemRequest(object_info=self._info.get('updateItem'))
    
    @update_item.setter
    def update_item(self, value: "UpdateItemRequest"):
        if self._info.get('updateItem',None) == value:
            return
        self._info['updateItem'] = value
        
    
    @property
    def update_settings(self)->"UpdateSettingsRequest":
        return UpdateSettingsRequest(object_info=self._info.get('updateSettings'))
    
    @update_settings.setter
    def update_settings(self, value: "UpdateSettingsRequest"):
        if self._info.get('updateSettings',None) == value:
            return
        self._info['updateSettings'] = value
        
    
    
    
    @property
    def wire_format(self)->dict:
        base = ''
        base = base[0].lower() + base[1:]
        request = self._info
        components = 'request'.split('_')
        # if it's an update, we need to provide an update mask
        # generate this automatically to cinlude all fields
        if components[0] == 'update':
            if not self.update_mask:
                target_field = [field for field in request.keys() if field not in ['update_mask', 'location']][0]           
                self._info['updateMask'] = ','.join(request[target_field].keys())
        return {base:self._info}
    
