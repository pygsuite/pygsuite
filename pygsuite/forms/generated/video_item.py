from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.video import Video


class VideoItem(BaseFormItem):
    """
    An item containing a video.
    """

    def __init__(  # noqa: C901
        self,
        caption: Optional[str] = None,
        video: Optional["Video"] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if caption is not None:

            generated["caption"] = caption
        if video is not None:

            generated["video"] = video._info
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def caption(self) -> str:
        return self._info.get("caption")

    @caption.setter
    def caption(self, value: str):
        if self._info.get("caption", None) == value:
            return
        self._info["caption"] = value

    @property
    def video(self) -> "Video":
        return Video(object_info=self._info.get("video"))

    @video.setter
    def video(self, value: "Video"):
        if self._info.get("video", None) == value:
            return
        self._info["video"] = value
