
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class RenewWatchRequest(BaseFormItem):
    """
    Renew an existing Watch for seven days.
    """
    def __init__(self, 
                object_info: Optional[Dict] = None):
        generated = {}
        
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    

