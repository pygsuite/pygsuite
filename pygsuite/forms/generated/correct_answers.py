from typing import Optional, Dict, List

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.correct_answer import CorrectAnswer


class CorrectAnswers(BaseFormItem):
    """
    The answer key for a question.
    """

    def __init__(
        self, answers: Optional[List["CorrectAnswer"]] = None, object_info: Optional[Dict] = None
    ):
        generated: Dict = {}

        if answers is not None:
            generated["answers"] = answers
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def answers(self) -> List["CorrectAnswer"]:
        return [CorrectAnswer(object_info=v) for v in self._info.get("answers")]

    @answers.setter
    def answers(self, value: List["CorrectAnswer"]):
        if self._info.get("answers", None) == value:
            return
        self._info["answers"] = value
