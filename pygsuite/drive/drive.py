from enum import Enum
from typing import Optional

from pygsuite import Clients

DRIVE_V3_API_URL = "https://www.googleapis.com/drive/v3/files"


class FileTypes(Enum):
    SHEETS = "application/vvnd.google-apps.spreadsheet"
    DOCS = "application/vnd.google-apps.document"
    SLIDES = "application/vnd.google-apps.slides"

    def __str__(self):
        return self.value


class Drive:
    def __init__(self, client=None):
        client = client or Clients.drive_client_v3
        self.service = client

    def find_files(self, type: FileTypes, name: Optional[str] = None):
        q = f'mimeType="{type}"'
        if name:
            q += f' and name = "{name}"'
        base = self.service.files().list(q=q).execute()
        files = base.get("files")
        page_token = base.get("nextPageToken")
        while page_token is not None:
            base = self.service.files().list(q=q).execute()
            files += base.get("files")
            page_token = base.get("nextPageToken")
        return files
