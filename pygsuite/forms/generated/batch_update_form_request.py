
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.request import Request
from pygsuite.forms.generated.write_control import WriteControl


class BatchUpdateFormRequest(BaseFormItem):
    """
    A batch of updates to perform on a form. All the specified updates are made or none of them are.
    """
    def __init__(self, 
                include_form_in_response: Optional[bool] = None,
                requests: Optional[List["Request"]] = None,
                write_control: Optional["WriteControl"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if include_form_in_response:
            generated['includeFormInResponse'] =  include_form_in_response 
        if requests:
            generated['requests'] =  requests 
        if write_control:
            generated['writeControl'] =  write_control._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def include_form_in_response(self)->bool:
        return self._info.get('includeFormInResponse')
    
    @include_form_in_response.setter
    def include_form_in_response(self, value: bool):
        if self._info['includeFormInResponse'] == value:
            return
        self._info['includeFormInResponse'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def requests(self)->List["Request"]:
        return [Request(object_info=v) for v in self._info.get('requests')]
        
    
    @requests.setter
    def requests(self, value: List["Request"]):
        if self._info['requests'] == value:
            return
        self._info['requests'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def write_control(self)->"WriteControl":
        return WriteControl(object_info=self._info.get('writeControl'))
    
    @write_control.setter
    def write_control(self, value: "WriteControl"):
        if self._info['writeControl'] == value:
            return
        self._info['writeControl'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

