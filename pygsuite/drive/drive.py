from enum import Enum
from typing import Optional

from pygsuite import Clients

DRIVE_V3_API_URL = "https://www.googleapis.com/drive/v3/files"


class PermissionType(Enum):
    OWNER = "owner"
    ORGANIZER = "organizer"
    FILE_ORGANIZER = "fileOrganizer"
    WRITER = "writer"
    COMMENTER = "commenter"
    READER = "reader"


class UserType(Enum):
    USER = "user"
    GROUP = "group"
    DOMAIN = "domain"
    ANYONE = "anyone"


class FileTypes(Enum):
    SHEETS = "application/vnd.google-apps.spreadsheet"
    DOCS = "application/vnd.google-apps.document"
    SLIDES = "application/vnd.google-apps.slides"

    def __str__(self):
        return self.value


def default_callback(request_id, response, exception):
    if exception:
        # Handle error
        raise ValueError(exception)
    print(request_id, response, exception)


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

    def update_file_permissions(
        self, file_id, address, role=PermissionType.READER, type=UserType.USER
    ):
        batch = self.service.new_batch_http_request(callback=default_callback)
        user_permission = {"type": type.value, "role": role.value, "emailAddress": address}
        batch.add(
            self.service.permissions().create(fileId=file_id, body=user_permission, fields="id")
        )
        batch.execute()
