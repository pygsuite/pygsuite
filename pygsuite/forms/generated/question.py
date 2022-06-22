from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.choice_question import ChoiceQuestion
from pygsuite.forms.generated.date_question import DateQuestion
from pygsuite.forms.generated.file_upload_question import FileUploadQuestion
from pygsuite.forms.generated.grading import Grading
from pygsuite.forms.generated.row_question import RowQuestion
from pygsuite.forms.generated.scale_question import ScaleQuestion
from pygsuite.forms.generated.text_question import TextQuestion
from pygsuite.forms.generated.time_question import TimeQuestion


class Question(BaseFormItem):
    """
    Any question. The specific type of question is known by its `kind`.
    """

    def __init__(  # noqa: C901
        self,
        choice_question: Optional["ChoiceQuestion"] = None,
        date_question: Optional["DateQuestion"] = None,
        file_upload_question: Optional["FileUploadQuestion"] = None,
        grading: Optional["Grading"] = None,
        question_id: Optional[str] = None,
        required: Optional[bool] = None,
        row_question: Optional["RowQuestion"] = None,
        scale_question: Optional["ScaleQuestion"] = None,
        text_question: Optional["TextQuestion"] = None,
        time_question: Optional["TimeQuestion"] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if choice_question is not None:
            generated["choiceQuestion"] = choice_question._info
        if date_question is not None:
            generated["dateQuestion"] = date_question._info
        if file_upload_question is not None:
            generated["fileUploadQuestion"] = file_upload_question._info
        if grading is not None:
            generated["grading"] = grading._info
        if question_id is not None:
            generated["questionId"] = question_id
        if required is not None:
            generated["required"] = required
        if row_question is not None:
            generated["rowQuestion"] = row_question._info
        if scale_question is not None:
            generated["scaleQuestion"] = scale_question._info
        if text_question is not None:
            generated["textQuestion"] = text_question._info
        if time_question is not None:
            generated["timeQuestion"] = time_question._info
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def choice_question(self) -> "ChoiceQuestion":
        return ChoiceQuestion(object_info=self._info.get("choiceQuestion"))

    @choice_question.setter
    def choice_question(self, value: "ChoiceQuestion"):
        if self._info.get("choiceQuestion", None) == value:
            return
        self._info["choiceQuestion"] = value

    @property
    def date_question(self) -> "DateQuestion":
        return DateQuestion(object_info=self._info.get("dateQuestion"))

    @date_question.setter
    def date_question(self, value: "DateQuestion"):
        if self._info.get("dateQuestion", None) == value:
            return
        self._info["dateQuestion"] = value

    @property
    def file_upload_question(self) -> "FileUploadQuestion":
        return FileUploadQuestion(object_info=self._info.get("fileUploadQuestion"))

    @file_upload_question.setter
    def file_upload_question(self, value: "FileUploadQuestion"):
        if self._info.get("fileUploadQuestion", None) == value:
            return
        self._info["fileUploadQuestion"] = value

    @property
    def grading(self) -> "Grading":
        return Grading(object_info=self._info.get("grading"))

    @grading.setter
    def grading(self, value: "Grading"):
        if self._info.get("grading", None) == value:
            return
        self._info["grading"] = value

    @property
    def question_id(self) -> str:
        return self._info.get("questionId")

    @question_id.setter
    def question_id(self, value: str):
        if self._info.get("questionId", None) == value:
            return
        self._info["questionId"] = value

    @property
    def required(self) -> bool:
        return self._info.get("required")

    @required.setter
    def required(self, value: bool):
        if self._info.get("required", None) == value:
            return
        self._info["required"] = value

    @property
    def row_question(self) -> "RowQuestion":
        return RowQuestion(object_info=self._info.get("rowQuestion"))

    @row_question.setter
    def row_question(self, value: "RowQuestion"):
        if self._info.get("rowQuestion", None) == value:
            return
        self._info["rowQuestion"] = value

    @property
    def scale_question(self) -> "ScaleQuestion":
        return ScaleQuestion(object_info=self._info.get("scaleQuestion"))

    @scale_question.setter
    def scale_question(self, value: "ScaleQuestion"):
        if self._info.get("scaleQuestion", None) == value:
            return
        self._info["scaleQuestion"] = value

    @property
    def text_question(self) -> "TextQuestion":
        return TextQuestion(object_info=self._info.get("textQuestion"))

    @text_question.setter
    def text_question(self, value: "TextQuestion"):
        if self._info.get("textQuestion", None) == value:
            return
        self._info["textQuestion"] = value

    @property
    def time_question(self) -> "TimeQuestion":
        return TimeQuestion(object_info=self._info.get("timeQuestion"))

    @time_question.setter
    def time_question(self, value: "TimeQuestion"):
        if self._info.get("timeQuestion", None) == value:
            return
        self._info["timeQuestion"] = value
