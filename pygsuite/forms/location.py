from .base_object import BaseFormItem

class Location(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def index(self):
        return self._info.get('index')
