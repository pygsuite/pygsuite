
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem


class CloudPubsubTopic(BaseFormItem):
    """
    A Pub/Sub topic.
    """
    def __init__(self, 
                topic_name: Optional[str] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if topic_name:
            generated['topicName'] =  topic_name 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def topic_name(self)->str:
        return self._info.get('topicName')
    
    @topic_name.setter
    def topic_name(self, value: str):
        if self._info['topicName'] == value:
            return
        self._info['topicName'] = value
        #self._form._mutation([UpdateItemRequest(item=self, location=self.location).request])
    

