
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class QuizSettings(BaseFormItem):
    """
    Settings related to quiz forms and grading. These must be updated with the UpdateSettingsRequest.
    """
    def __init__(self, 
                is_quiz: Optional[bool] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if is_quiz:
            generated['isQuiz'] =  is_quiz 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def is_quiz(self)->bool:
        return self._info.get('isQuiz')
    
    @is_quiz.setter
    def is_quiz(self, value: bool):
        if self._info['isQuiz'] == value:
            return
        self._info['isQuiz'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

