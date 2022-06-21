
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class PageBreakItem(BaseFormItem):
    """
    A page break. The title and description of this item are shown at the top of the new page.
    """
    def __init__(self, 
                object_info: Optional[Dict] = None):
        generated = {}
        
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    
    
