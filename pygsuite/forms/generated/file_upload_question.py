
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class FileUploadQuestion(BaseFormItem):
    """
    A file upload question. The API currently does not support creating file upload questions.
    """
    def __init__(self, 
                folder_id: Optional[str] = None,
                max_file_size: Optional[str] = None,
                max_files: Optional[int] = None,
                types: Optional[List["str"]] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if folder_id:
            generated['folderId'] =  folder_id 
        if max_file_size:
            generated['maxFileSize'] =  max_file_size 
        if max_files:
            generated['maxFiles'] =  max_files 
        if types:
            generated['types'] =  types 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def folder_id(self)->str:
        return self._info.get('folderId')
    
    @folder_id.setter
    def folder_id(self, value: str):
        if self._info['folderId'] == value:
            return
        self._info['folderId'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def max_file_size(self)->str:
        return self._info.get('maxFileSize')
    
    @max_file_size.setter
    def max_file_size(self, value: str):
        if self._info['maxFileSize'] == value:
            return
        self._info['maxFileSize'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def max_files(self)->int:
        return self._info.get('maxFiles')
    
    @max_files.setter
    def max_files(self, value: int):
        if self._info['maxFiles'] == value:
            return
        self._info['maxFiles'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def types(self)->List["str"]:
        return [v for v in self._info.get('types')]
        
    
    @types.setter
    def types(self, value: List["str"]):
        if self._info['types'] == value:
            return
        self._info['types'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

