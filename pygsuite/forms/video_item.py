from .base_object import BaseFormItem

class VideoItem(BaseFormItem):
    def __init__(self, info: dict, form):
        super().__init__(info, form)

    @property
    def video(self):
        return self._info.get('video')


    @property
    def caption(self):
        return self._info.get('caption')

