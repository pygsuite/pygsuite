from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.info import Info


class UpdateFormInfoRequest(BaseFormItem):
    """
    Update Form's Info.
    """

    def __init__(
        self,
        info: Optional["Info"] = None,
        update_mask: Optional[str] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if info is not None:
            generated["info"] = info._info
        if update_mask is not None:
            generated["updateMask"] = update_mask
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def info(self) -> "Info":
        return Info(object_info=self._info.get("info"))

    @info.setter
    def info(self, value: "Info"):
        if self._info.get("info", None) == value:
            return
        self._info["info"] = value

    @property
    def update_mask(self) -> str:
        return self._info.get("updateMask")

    @update_mask.setter
    def update_mask(self, value: str):
        if self._info.get("updateMask", None) == value:
            return
        self._info["updateMask"] = value

    @property
    def wire_format(self) -> dict:
        base = "UpdateFormInfo"
        base = base[0].lower() + base[1:]

        request = self._info
        components = "update_form_info_request".split("_")
        # if it's an update, we *may* need to provide an update mask
        # generate this automatically to include all fields
        # can be optionally overridden when creating synchronization method
        if components[0] == "update":
            if not self.update_mask:
                target_field = [
                    field for field in request.keys() if field not in ["update_mask", "location"]
                ][0]
                self._info["updateMask"] = ",".join(request[target_field].keys())

        return {base: self._info}
