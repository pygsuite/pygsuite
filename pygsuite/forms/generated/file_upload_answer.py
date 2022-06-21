
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class FileUploadAnswer(BaseFormItem):
    """
    Info for a single file submitted to a file upload question.
    """
    def __init__(self, 
                object_info: Optional[Dict] = None):
        generated = {}
        
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def file_id(self)->str:
        return self._info.get('fileId')
    
    @property
    def file_name(self)->str:
        return self._info.get('fileName')
    
    @property
    def mime_type(self)->str:
        return self._info.get('mimeType')
    
    
    
