from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem


class TextItem(BaseFormItem):
    """
    A text item.
    """

    def __init__(self, object_info: Optional[Dict] = None):
        generated: Dict = {}

        object_info = object_info or generated
        super().__init__(object_info=object_info)
