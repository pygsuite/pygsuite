from typing import TYPE_CHECKING, Optional, Dict

from .base_object import BaseFormItem

if TYPE_CHECKING:
    from pygsuite.forms import Form


class PageBreakItem(BaseFormItem):
    def __init__(self, form: Optional["Form"] = None, info: Optional[Dict] = None):
        info = info or {}
        super().__init__(info=info, form=form)
