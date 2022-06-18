from .base_object import BaseFormItem

class DateQuestion(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def include_time(self):
        return self._info.get('includeTime')

    @include_time.setter
    def include_time(self, value):
        self._info['includeTime'] = value


    @property
    def include_year(self):
        return self._info.get('includeYear')

    @include_year.setter
    def include_year(self, value):
        self._info['includeYear'] = value