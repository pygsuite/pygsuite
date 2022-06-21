
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.choice_question import ChoiceQuestion


class Grid(BaseFormItem):
    """
    A grid of choices (radio or check boxes) with each row constituting a separate question. Each row has the same choices, which are shown as the columns.
    """
    def __init__(self, 
                columns: Optional["ChoiceQuestion"] = None,
                shuffle_questions: Optional[bool] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if columns is not None:
            generated['columns'] =  columns._info 
        if shuffle_questions is not None:
            generated['shuffleQuestions'] =  shuffle_questions 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def columns(self)->"ChoiceQuestion":
        return ChoiceQuestion(object_info=self._info.get('columns'))
    
    @columns.setter
    def columns(self, value: "ChoiceQuestion"):
        if self._info.get('columns',None) == value:
            return
        self._info['columns'] = value
        
    
    @property
    def shuffle_questions(self)->bool:
        return self._info.get('shuffleQuestions')
    
    @shuffle_questions.setter
    def shuffle_questions(self, value: bool):
        if self._info.get('shuffleQuestions',None) == value:
            return
        self._info['shuffleQuestions'] = value
        
    
    
    
