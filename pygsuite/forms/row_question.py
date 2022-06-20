from typing import TYPE_CHECKING, Optional, Dict

from .base_object import BaseFormItem

if TYPE_CHECKING:
    from pygsuite.forms import Form


class RowQuestion(BaseFormItem):
    def __init__(self, title:str = None,
                 form: Optional["Form"] = None, info: Optional[Dict] = None):
        generated = {}
        if title is not None:
            generated['title'] = title
        info = info or generated
        super().__init__(info=info, form=form)

    @property
    def title(self) -> bool:
        return bool(self._info.get('title', False))
