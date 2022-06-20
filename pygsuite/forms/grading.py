from typing import TYPE_CHECKING, Optional, Dict, Union

from .base_object import BaseFormItem

if TYPE_CHECKING:
    from pygsuite.forms import Form
    from pygsuite.forms.image import Image
    from pygsuite.forms.question import Question


class Grading(BaseFormItem):
    def __init__(self,
                 form: Optional["Form"] = None, info: Optional[Dict] = None):
        generated = {}
        info = info or generated
        super().__init__(info=info, form=form)
