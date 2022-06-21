
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class FormResponse(BaseFormItem):
    """
    A form response.
    """
    def __init__(self, 
                object_info: Optional[Dict] = None):
        generated = {}
        
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def answers(self)->object:
        return self._info.get('answers')
    
    @property
    def create_time(self)->str:
        return self._info.get('createTime')
    
    @property
    def form_id(self)->str:
        return self._info.get('formId')
    
    @property
    def last_submitted_time(self)->str:
        return self._info.get('lastSubmittedTime')
    
    @property
    def respondent_email(self)->str:
        return self._info.get('respondentEmail')
    
    @property
    def response_id(self)->str:
        return self._info.get('responseId')
    
    @property
    def total_score(self)->number:
        return self._info.get('totalScore')
    
    
    
