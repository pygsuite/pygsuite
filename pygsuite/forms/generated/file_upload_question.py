from typing import Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class FileUploadQuestion(BaseFormItem):
    """
    A file upload question. The API currently does not support creating file upload questions.
    """

    def __init__(
        self,
        folder_id: Optional[str] = None,
        max_file_size: Optional[str] = None,
        max_files: Optional[int] = None,
        types: Optional[List["str"]] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if folder_id is not None:

            generated["folderId"] = folder_id
        if max_file_size is not None:

            generated["maxFileSize"] = max_file_size
        if max_files is not None:

            generated["maxFiles"] = max_files
        if types is not None:
            generated["types"] = [v for v in types]
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def folder_id(self) -> str:
        return self._info.get("folderId")

    @folder_id.setter
    def folder_id(self, value: str):
        if self._info.get("folderId", None) == value:
            return
        self._info["folderId"] = value

    @property
    def max_file_size(self) -> str:
        return self._info.get("maxFileSize")

    @max_file_size.setter
    def max_file_size(self, value: str):
        if self._info.get("maxFileSize", None) == value:
            return
        self._info["maxFileSize"] = value

    @property
    def max_files(self) -> int:
        return self._info.get("maxFiles")

    @max_files.setter
    def max_files(self, value: int):
        if self._info.get("maxFiles", None) == value:
            return
        self._info["maxFiles"] = value

    @property
    def types(self) -> List["str"]:
        return [v for v in self._info.get("types")]

    @types.setter
    def types(self, value: List["str"]):
        if self._info.get("types", None) == value:
            return
        self._info["types"] = value
