from typing import TYPE_CHECKING, Optional, Dict

from .base_object import BaseFormItem

if TYPE_CHECKING:
    from pygsuite.forms import Form


class TextItem(BaseFormItem):
    def __init__(self, form: Optional["Form"] = None, info: Optional[Dict] = None, **kwargs):
        info = info or {}
        super().__init__(info=info, form=form)
