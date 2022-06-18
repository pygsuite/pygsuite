from .base_object import BaseFormItem
from .media_properties import MediaProperties
class Image(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def content_uri(self):
        return self._info.get('contentUri')


    @property
    def alt_text(self):
        return self._info.get('altText')


    @property
    def properties(self):
        return MediaProperties(self._info.get('properties'), self._form)


    @property
    def source_uri(self):
        return self._info.get('sourceUri')
