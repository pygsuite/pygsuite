from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem


class WriteControl(BaseFormItem):
    """
    Provides control over how write requests are executed.
    """

    def __init__(
        self,  # noqa: C901
        required_revision_id: Optional[str] = None,
        target_revision_id: Optional[str] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if required_revision_id is not None:

            generated["requiredRevisionId"] = required_revision_id
        if target_revision_id is not None:

            generated["targetRevisionId"] = target_revision_id
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def required_revision_id(self) -> str:
        return self._info.get("requiredRevisionId")

    @required_revision_id.setter
    def required_revision_id(self, value: str):
        if self._info.get("requiredRevisionId", None) == value:
            return
        self._info["requiredRevisionId"] = value

    @property
    def target_revision_id(self) -> str:
        return self._info.get("targetRevisionId")

    @target_revision_id.setter
    def target_revision_id(self, value: str):
        if self._info.get("targetRevisionId", None) == value:
            return
        self._info["targetRevisionId"] = value
