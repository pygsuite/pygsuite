from typing import Optional, Dict, List

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.option import Option


class ChoiceQuestion(BaseFormItem):
    """
    A radio/checkbox/dropdown question.
    """

    def __init__(
        self,
        options: Optional[List["Option"]] = None,
        shuffle: Optional[bool] = None,
        type: Optional[str] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if options is not None:
            generated["options"] = [v._info for v in options]
        if shuffle is not None:

            generated["shuffle"] = shuffle
        if type is not None:

            generated["type"] = type
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def options(self) -> List["Option"]:
        return [Option(object_info=v) for v in self._info.get("options")]

    @options.setter
    def options(self, value: List["Option"]):
        if self._info.get("options", None) == value:
            return
        self._info["options"] = value

    @property
    def shuffle(self) -> bool:
        return self._info.get("shuffle")

    @shuffle.setter
    def shuffle(self, value: bool):
        if self._info.get("shuffle", None) == value:
            return
        self._info["shuffle"] = value

    @property
    def type(self) -> str:
        return self._info.get("type")

    @type.setter
    def type(self, value: str):
        if self._info.get("type", None) == value:
            return
        self._info["type"] = value
