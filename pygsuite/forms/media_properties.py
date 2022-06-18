from .base_object import BaseFormItem

class MediaProperties(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def alignment(self):
        return self._info.get('alignment')


    @property
    def width(self):
        return self._info.get('width')

