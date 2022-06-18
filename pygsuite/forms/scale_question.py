
from .base_object import BaseFormItem

class ScaleQuestion(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def low(self)->int:
        return self._info.get('low')


    @property
    def high(self)->int:
        return self._info.get('high')


    @property
    def low_label(self)->str:
        return self._info.get('lowLabel')


    @property
    def high_label(self)->str:
        return self._info.get('highLabel')

