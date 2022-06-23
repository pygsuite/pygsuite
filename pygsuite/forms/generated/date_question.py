from typing import Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class DateQuestion(BaseFormItem):
    """
    A date question. Date questions default to just month + day.
    """

    def __init__(
        self,
        include_time: Optional[bool] = None,
        include_year: Optional[bool] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if include_time is not None:

            generated["includeTime"] = include_time
        if include_year is not None:

            generated["includeYear"] = include_year
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def include_time(self) -> bool:
        return self._info.get("includeTime")

    @include_time.setter
    def include_time(self, value: bool):
        if self._info.get("includeTime", None) == value:
            return
        self._info["includeTime"] = value

    @property
    def include_year(self) -> bool:
        return self._info.get("includeYear")

    @include_year.setter
    def include_year(self, value: bool):
        if self._info.get("includeYear", None) == value:
            return
        self._info["includeYear"] = value
