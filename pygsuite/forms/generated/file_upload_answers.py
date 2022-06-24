from typing import Optional, Dict, List

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.file_upload_answer import FileUploadAnswer


class FileUploadAnswers(BaseFormItem):
    """
    All submitted files for a FileUpload question.
    """

    def __init__(self, object_info: Optional[Dict] = None):  # noqa: C901
        generated: Dict = {}

        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def answers(self) -> List["FileUploadAnswer"]:
        return [FileUploadAnswer(object_info=v) for v in self._info.get("answers", [])]
