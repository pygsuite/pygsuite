from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.correct_answers import CorrectAnswers
from pygsuite.forms.generated.feedback import Feedback


class Grading(BaseFormItem):
    """
    Grading for a single question
    """

    def __init__(
        self,
        correct_answers: Optional["CorrectAnswers"] = None,
        general_feedback: Optional["Feedback"] = None,
        point_value: Optional[int] = None,
        when_right: Optional["Feedback"] = None,
        when_wrong: Optional["Feedback"] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if correct_answers is not None:

            generated["correctAnswers"] = correct_answers._info
        if general_feedback is not None:

            generated["generalFeedback"] = general_feedback._info
        if point_value is not None:

            generated["pointValue"] = point_value
        if when_right is not None:

            generated["whenRight"] = when_right._info
        if when_wrong is not None:

            generated["whenWrong"] = when_wrong._info
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def correct_answers(self) -> "CorrectAnswers":
        return CorrectAnswers(object_info=self._info.get("correctAnswers"))

    @correct_answers.setter
    def correct_answers(self, value: "CorrectAnswers"):
        if self._info.get("correctAnswers", None) == value:
            return
        self._info["correctAnswers"] = value

    @property
    def general_feedback(self) -> "Feedback":
        return Feedback(object_info=self._info.get("generalFeedback"))

    @general_feedback.setter
    def general_feedback(self, value: "Feedback"):
        if self._info.get("generalFeedback", None) == value:
            return
        self._info["generalFeedback"] = value

    @property
    def point_value(self) -> int:
        return self._info.get("pointValue")

    @point_value.setter
    def point_value(self, value: int):
        if self._info.get("pointValue", None) == value:
            return
        self._info["pointValue"] = value

    @property
    def when_right(self) -> "Feedback":
        return Feedback(object_info=self._info.get("whenRight"))

    @when_right.setter
    def when_right(self, value: "Feedback"):
        if self._info.get("whenRight", None) == value:
            return
        self._info["whenRight"] = value

    @property
    def when_wrong(self) -> "Feedback":
        return Feedback(object_info=self._info.get("whenWrong"))

    @when_wrong.setter
    def when_wrong(self, value: "Feedback"):
        if self._info.get("whenWrong", None) == value:
            return
        self._info["whenWrong"] = value
