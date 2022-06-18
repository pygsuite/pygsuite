from .base_object import BaseFormItem

class PageBreakItem(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)