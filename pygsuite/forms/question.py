from typing import TYPE_CHECKING, Optional, Dict, Union

from .base_object import BaseFormItem

if TYPE_CHECKING:
    from pygsuite.forms import Form
    from pygsuite.forms.image import Image
    from pygsuite.forms.grading import Grading
    from pygsuite.forms.date_question import DateQuestion
    from pygsuite.forms.text_question import TextQuestion

from pygsuite.forms.enums import QuestionType
class Question(BaseFormItem):
    def __init__(self, required:Optional[bool] = False,
                 question_detail: Optional[Union["DateQuestion", "TextQuestion"]]=None,
                 grading: Optional["Grading"] = None,
                 form: Optional["Form"] = None, info: Optional[Dict] = None):
        generated = {}
        if question_detail:
            generated[QuestionType(question_detail).value] = question_detail._info
        if required:
            generated['required'] = required
        if grading:
            generated['grading'] = grading._info
        info = info or generated
        super().__init__(info=info, form=form)

    @property
    def question(self):
        return self._info.get('question')

    @property
    def image(self):
        return self._info.get('image')
