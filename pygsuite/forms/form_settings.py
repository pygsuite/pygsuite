from .quiz_settings import QuizSettings

class FormSettings(object):
    def __init__(self, info: dict, form):
        self._info = info
        self._form = form

    @property
    def quiz_settings(self):
        return QuizSettings(self._info.get('quiz_settings'), self._form)