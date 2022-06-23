from typing import Optional, Dict

from pygsuite.forms.base_object import BaseFormItem
from pygsuite.forms.generated.media_properties import MediaProperties


class Video(BaseFormItem):
    """
    Data representing a video.
    """

    def __init__(
        self,
        properties: Optional["MediaProperties"] = None,
        youtube_uri: Optional[str] = None,
        object_info: Optional[Dict] = None,
    ):
        generated: Dict = {}

        if properties is not None:

            generated["properties"] = properties._info
        if youtube_uri is not None:

            generated["youtubeUri"] = youtube_uri
        object_info = object_info or generated
        super().__init__(object_info=object_info)

    @property
    def properties(self) -> "MediaProperties":
        return MediaProperties(object_info=self._info.get("properties"))

    @properties.setter
    def properties(self, value: "MediaProperties"):
        if self._info.get("properties", None) == value:
            return
        self._info["properties"] = value

    @property
    def youtube_uri(self) -> str:
        return self._info.get("youtubeUri")

    @youtube_uri.setter
    def youtube_uri(self, value: str):
        if self._info.get("youtubeUri", None) == value:
            return
        self._info["youtubeUri"] = value
