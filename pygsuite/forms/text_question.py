from typing import TYPE_CHECKING, Optional, Dict

from .base_object import BaseFormItem

if TYPE_CHECKING:
    from pygsuite.forms import Form


class TextQuestion(BaseFormItem):
    def __init__(self, paragraph: bool = False,
                 form: Optional["Form"] = None, info: Optional[Dict] = None):
        generated = {}
        if paragraph is not None:
            generated['paragraph'] = paragraph
        info = info or generated
        super().__init__(info=info, form=form)

    @property
    def paragraph(self) -> bool:
        return bool(self._info.get('paragraph'))
