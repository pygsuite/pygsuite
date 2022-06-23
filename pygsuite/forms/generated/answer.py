from typing import Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.file_upload_answers import FileUploadAnswers
from pygsuite.forms.generated.grade import Grade
from pygsuite.forms.generated.text_answers import TextAnswers


class Answer(BaseFormItem):
    """
    The submitted answer for a question.
    """

    def __init__(self, object_info: Optional[Dict] = None):
        generated: Dict = {}

        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def file_upload_answers(self) -> "FileUploadAnswers":
        return FileUploadAnswers(object_info=self._info.get("fileUploadAnswers"))

    @property
    def grade(self) -> "Grade":
        return Grade(object_info=self._info.get("grade"))

    @property
    def question_id(self) -> str:
        return self._info.get("questionId")

    @property
    def text_answers(self) -> "TextAnswers":
        return TextAnswers(object_info=self._info.get("textAnswers"))
