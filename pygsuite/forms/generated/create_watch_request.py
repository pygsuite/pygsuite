from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.watch import Watch


class CreateWatchRequest(BaseFormItem):
    """
    Create a new watch.
    """

    def __init__(  # noqa: C901
        self,
        watch: Optional["Watch"] = None,
        watch_id: Optional[str] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if watch is not None:

            generated["watch"] = watch._info
        if watch_id is not None:

            generated["watchId"] = watch_id
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def watch(self) -> "Watch":
        return Watch(object_info=self._info.get("watch"))

    @watch.setter
    def watch(self, value: "Watch"):
        if self._info.get("watch", None) == value:
            return
        self._info["watch"] = value

    @property
    def watch_id(self) -> str:
        return self._info.get("watchId")

    @watch_id.setter
    def watch_id(self, value: str):
        if self._info.get("watchId", None) == value:
            return
        self._info["watchId"] = value

    @property
    def wire_format(self) -> dict:
        base = "CreateWatch"
        base = base[0].lower() + base[1:]

        return {base: self._info}
