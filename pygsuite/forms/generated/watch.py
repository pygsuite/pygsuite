from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.watch_target import WatchTarget


class Watch(BaseFormItem):
    """
    A watch for events for a form. When the designated event happens, a notification will be published to the specified target. The notification's attributes will include a `formId` key that has the ID of the watched form and an `eventType` key that has the string of the type. Messages are sent with at-least-once delivery and are only dropped in extraordinary circumstances. Typically all notifications should be reliably delivered within a few seconds; however, in some situations notifications may be delayed. A watch expires seven days after it is created unless it is renewed with watches.renew
    """

    def __init__(
        self,
        event_type: Optional[str] = None,
        target: Optional["WatchTarget"] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if event_type is not None:
            generated["eventType"] = event_type
        if target is not None:
            generated["target"] = target._info
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def create_time(self) -> str:
        return self._info.get("createTime")

    @property
    def error_type(self) -> str:
        return self._info.get("errorType")

    @property
    def event_type(self) -> str:
        return self._info.get("eventType")

    @event_type.setter
    def event_type(self, value: str):
        if self._info.get("eventType", None) == value:
            return
        self._info["eventType"] = value

    @property
    def expire_time(self) -> str:
        return self._info.get("expireTime")

    @property
    def id(self) -> str:
        return self._info.get("id")

    @property
    def state(self) -> str:
        return self._info.get("state")

    @property
    def target(self) -> "WatchTarget":
        return WatchTarget(object_info=self._info.get("target"))

    @target.setter
    def target(self, value: "WatchTarget"):
        if self._info.get("target", None) == value:
            return
        self._info["target"] = value
