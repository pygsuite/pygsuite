from typing import Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class Empty(BaseFormItem):
    """
    A generic empty message that you can re-use to avoid defining duplicated empty messages in your APIs. A typical example is to use it as the request or the response type of an API method. For instance: service Foo { rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty); }
    """

    def __init__(self, object_info: Optional[Dict] = None):
        generated: Dict = {}

        object_info = object_info or generated
        super().__init__(object_info=object_info)
