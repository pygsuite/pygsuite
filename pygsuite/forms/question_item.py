from typing import TYPE_CHECKING, Optional, Dict, Union

from .base_object import BaseFormItem

if TYPE_CHECKING:
    from pygsuite.forms import Form
    from pygsuite.forms.image import Image
    from pygsuite.forms.question import Question


class QuestionItem(BaseFormItem):
    def __init__(self, question: Optional["Question"] = None,
                 image: Optional["Image"] = None,
                 form: Optional["Form"] = None, info: Optional[Dict] = None):
        generated = {}
        if question:
            generated['question'] = question._info
        if image:
            generated['image'] = image._info
        info = info or generated
        super().__init__(info=info, form=form)

    @property
    def question(self):
        return self._info.get('question')

    @property
    def image(self):
        return self._info.get('image')
