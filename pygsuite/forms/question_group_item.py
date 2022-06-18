from .base_object import BaseFormItem

class QuestionGroupItem(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def questions(self):
        return self._info.get('questions')


    @property
    def image(self):
        return self._info.get('image')


    @property
    def grid(self):
        return self._info.get('grid')