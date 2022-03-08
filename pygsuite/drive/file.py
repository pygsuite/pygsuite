from typing import Optional

from googleapiclient.discovery import Resource

from pygsuite.common.parsing import parse_id
from pygsuite.drive.drive_object import DriveObject
from pygsuite.enums import MimeType


class File(DriveObject):
    """Base class for a Google Drive File"""

    _mimetype = MimeType.UNKNOWN
    _base_url = "https://drive.google.com/file/d/{}/view"

    def __init__(self, id: str = None, client: Optional[Resource] = None):

        self.id = parse_id(id) if id else None
        self.client = client

        DriveObject.__init__(self, id=id, client=client)
