from typing import Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.text_answer import TextAnswer


class TextAnswers(BaseFormItem):
    """
    A question's answers as text.
    """

    def __init__(self, object_info: Optional[Dict] = None):
        generated: Dict = {}

        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def answers(self) -> List["TextAnswer"]:
        return [TextAnswer(object_info=v) for v in self._info.get("answers")]
