from .base_object import BaseFormItem

class ImageItem(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def image(self):
        return self._info.get('image')
