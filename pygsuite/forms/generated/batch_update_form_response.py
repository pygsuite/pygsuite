from typing import Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.form import Form
from pygsuite.forms.generated.response import Response
from pygsuite.forms.generated.write_control import WriteControl


class BatchUpdateFormResponse(BaseFormItem):
    """
    Response to a BatchUpdateFormRequest.
    """

    def __init__(
        self,
        form: Optional["Form"] = None,
        replies: Optional[List["Response"]] = None,
        write_control: Optional["WriteControl"] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if form is not None:

            generated["form"] = form._info
        if replies is not None:
            generated["replies"] = [v._info for v in replies]
        if write_control is not None:

            generated["writeControl"] = write_control._info
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def form(self) -> "Form":
        return Form(object_info=self._info.get("form"))

    @form.setter
    def form(self, value: "Form"):
        if self._info.get("form", None) == value:
            return
        self._info["form"] = value

    @property
    def replies(self) -> List["Response"]:
        return [Response(object_info=v) for v in self._info.get("replies")]

    @replies.setter
    def replies(self, value: List["Response"]):
        if self._info.get("replies", None) == value:
            return
        self._info["replies"] = value

    @property
    def write_control(self) -> "WriteControl":
        return WriteControl(object_info=self._info.get("writeControl"))

    @write_control.setter
    def write_control(self, value: "WriteControl"):
        if self._info.get("writeControl", None) == value:
            return
        self._info["writeControl"] = value
