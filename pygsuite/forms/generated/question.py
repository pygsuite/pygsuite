
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.choice_question import ChoiceQuestion
from pygsuite.forms.generated.date_question import DateQuestion
from pygsuite.forms.generated.file_upload_question import FileUploadQuestion
from pygsuite.forms.generated.grading import Grading
from pygsuite.forms.generated.row_question import RowQuestion
from pygsuite.forms.generated.scale_question import ScaleQuestion
from pygsuite.forms.generated.text_question import TextQuestion
from pygsuite.forms.generated.time_question import TimeQuestion


class Question(BaseFormItem):
    """
    Any question. The specific type of question is known by its `kind`.
    """
    def __init__(self, 
                choice_question: Optional["ChoiceQuestion"] = None,
                date_question: Optional["DateQuestion"] = None,
                file_upload_question: Optional["FileUploadQuestion"] = None,
                grading: Optional["Grading"] = None,
                question_id: Optional[str] = None,
                required: Optional[bool] = None,
                row_question: Optional["RowQuestion"] = None,
                scale_question: Optional["ScaleQuestion"] = None,
                text_question: Optional["TextQuestion"] = None,
                time_question: Optional["TimeQuestion"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if choice_question:
            generated['choiceQuestion'] =  choice_question._info 
        if date_question:
            generated['dateQuestion'] =  date_question._info 
        if file_upload_question:
            generated['fileUploadQuestion'] =  file_upload_question._info 
        if grading:
            generated['grading'] =  grading._info 
        if question_id:
            generated['questionId'] =  question_id 
        if required:
            generated['required'] =  required 
        if row_question:
            generated['rowQuestion'] =  row_question._info 
        if scale_question:
            generated['scaleQuestion'] =  scale_question._info 
        if text_question:
            generated['textQuestion'] =  text_question._info 
        if time_question:
            generated['timeQuestion'] =  time_question._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def choice_question(self)->"ChoiceQuestion":
        return ChoiceQuestion(object_info=self._info.get('choiceQuestion'))
    
    @choice_question.setter
    def choice_question(self, value: "ChoiceQuestion"):
        if self._info['choiceQuestion'] == value:
            return
        self._info['choiceQuestion'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def date_question(self)->"DateQuestion":
        return DateQuestion(object_info=self._info.get('dateQuestion'))
    
    @date_question.setter
    def date_question(self, value: "DateQuestion"):
        if self._info['dateQuestion'] == value:
            return
        self._info['dateQuestion'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def file_upload_question(self)->"FileUploadQuestion":
        return FileUploadQuestion(object_info=self._info.get('fileUploadQuestion'))
    
    @file_upload_question.setter
    def file_upload_question(self, value: "FileUploadQuestion"):
        if self._info['fileUploadQuestion'] == value:
            return
        self._info['fileUploadQuestion'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def grading(self)->"Grading":
        return Grading(object_info=self._info.get('grading'))
    
    @grading.setter
    def grading(self, value: "Grading"):
        if self._info['grading'] == value:
            return
        self._info['grading'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def question_id(self)->str:
        return self._info.get('questionId')
    
    @question_id.setter
    def question_id(self, value: str):
        if self._info['questionId'] == value:
            return
        self._info['questionId'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def required(self)->bool:
        return self._info.get('required')
    
    @required.setter
    def required(self, value: bool):
        if self._info['required'] == value:
            return
        self._info['required'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def row_question(self)->"RowQuestion":
        return RowQuestion(object_info=self._info.get('rowQuestion'))
    
    @row_question.setter
    def row_question(self, value: "RowQuestion"):
        if self._info['rowQuestion'] == value:
            return
        self._info['rowQuestion'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def scale_question(self)->"ScaleQuestion":
        return ScaleQuestion(object_info=self._info.get('scaleQuestion'))
    
    @scale_question.setter
    def scale_question(self, value: "ScaleQuestion"):
        if self._info['scaleQuestion'] == value:
            return
        self._info['scaleQuestion'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def text_question(self)->"TextQuestion":
        return TextQuestion(object_info=self._info.get('textQuestion'))
    
    @text_question.setter
    def text_question(self, value: "TextQuestion"):
        if self._info['textQuestion'] == value:
            return
        self._info['textQuestion'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    
    @property
    def time_question(self)->"TimeQuestion":
        return TimeQuestion(object_info=self._info.get('timeQuestion'))
    
    @time_question.setter
    def time_question(self, value: "TimeQuestion"):
        if self._info['timeQuestion'] == value:
            return
        self._info['timeQuestion'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

