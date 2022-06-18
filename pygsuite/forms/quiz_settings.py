

class QuizSettings(object):
    def __init__(self, info: dict, form):
        self._info = info
        self._form = form

    @property
    def is_quiz(self):
        return self._info.get('isQuiz')
