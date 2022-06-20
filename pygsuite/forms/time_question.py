from typing import TYPE_CHECKING, Optional, Dict

from .base_object import BaseFormItem

if TYPE_CHECKING:
    from pygsuite.forms import Form


class TimeQuestion(BaseFormItem):
    def __init__(self, duration: bool = False,
                 form: Optional["Form"] = None, info: Optional[Dict] = None):
        generated = {}
        if duration is not None:
            generated['duration'] = duration
        info = info or generated
        super().__init__(info=info, form=form)

    @property
    def duration(self) -> bool:
        return bool(self._info.get('duration', False))
