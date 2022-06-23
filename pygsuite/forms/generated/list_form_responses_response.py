from typing import Optional, Dict, List

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.form_response import FormResponse


class ListFormResponsesResponse(BaseFormItem):
    """
    Response to a ListFormResponsesRequest.
    """

    def __init__(
        self,
        next_page_token: Optional[str] = None,
        responses: Optional[List["FormResponse"]] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if next_page_token is not None:

            generated["nextPageToken"] = next_page_token
        if responses is not None:
            generated["responses"] = [v._info for v in responses]
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def next_page_token(self) -> str:
        return self._info.get("nextPageToken")

    @next_page_token.setter
    def next_page_token(self, value: str):
        if self._info.get("nextPageToken", None) == value:
            return
        self._info["nextPageToken"] = value

    @property
    def responses(self) -> List["FormResponse"]:
        return [FormResponse(object_info=v) for v in self._info.get("responses")]

    @responses.setter
    def responses(self, value: List["FormResponse"]):
        if self._info.get("responses", None) == value:
            return
        self._info["responses"] = value
