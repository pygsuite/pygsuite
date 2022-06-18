
from .base_object import BaseFormItem

class TextQuestion(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def paragraph(self)->bool:
        return bool(self._info.get('paragraph'))
