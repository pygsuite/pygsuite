
from typing import TYPE_CHECKING, Optional, Dict, Union, List

from pygsuite.forms.base_object import BaseFormItem

from pygsuite.forms.generated.cloud_pubsub_topic import CloudPubsubTopic


class WatchTarget(BaseFormItem):
    """
    The target for notification delivery.
    """
    def __init__(self, 
                topic: Optional["CloudPubsubTopic"] = None,
                object_info: Optional[Dict] = None):
        generated = {}
        
        if topic is not None:
            generated['topic'] =  topic._info 
        object_info = object_info or generated
        super().__init__(object_info=object_info)
    
    
    @property
    def topic(self)->"CloudPubsubTopic":
        return CloudPubsubTopic(object_info=self._info.get('topic'))
    
    @topic.setter
    def topic(self, value: "CloudPubsubTopic"):
        if self._info.get('topic',None) == value:
            return
        self._info['topic'] = value
        
    
    
    
