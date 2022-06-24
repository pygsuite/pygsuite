from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem


class RenewWatchRequest(BaseFormItem):
    """
    Renew an existing Watch for seven days.
    """

    def __init__(self, object_info: Optional[Dict] = None):  # noqa: C901
        generated: Dict = {}

        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def wire_format(self) -> dict:
        base = "RenewWatch"
        base = base[0].lower() + base[1:]

        return {base: self._info}
