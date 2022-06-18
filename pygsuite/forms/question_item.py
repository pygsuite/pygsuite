from .base_object import BaseFormItem

class QuestionItem(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def question(self):
        return self._info.get('question')


    @property
    def image(self):
        return self._info.get('image')
