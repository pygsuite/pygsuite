from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.feedback import Feedback


class Grade(BaseFormItem):
    """
    Grade information associated with a respondent's answer to a question.
    """

    def __init__(self, object_info: Optional[Dict] = None):  # noqa: C901
        generated: Dict = {}

        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def correct(self) -> bool:
        return self._info.get("correct")

    @property
    def feedback(self) -> "Feedback":
        return Feedback(object_info=self._info.get("feedback"))

    @property
    def score(self) -> float:
        return self._info.get("score")
