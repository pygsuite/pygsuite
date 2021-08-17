from typing import List

from pygsuite import Clients
from pygsuite.common.comment import Comment
from pygsuite.utility.decorators import lazy_property


class DriveObject:

    def __init__(self, id, client):
        self.id = id
        self.client = client

    @property
    def comments(self) -> List[Comment]:
        return [Comment(item) for item in
                self.drive_client.comments().list(fileId=self.id).execute().get('items', [])]

    @lazy_property
    def drive_client(self):
        return Clients.drive_client_v2

    @classmethod
    def create_new(cls, title: str, client=None):
        raise NotImplementedError

    @classmethod
    def get_safe(cls, title: str, drive_client=None, object_client=None):
        from pygsuite.drive import Drive, FileTypes

        file_client = drive_client or Clients.drive_client_v3
        files = Drive(client=file_client).find_files(FileTypes.DOCS, name=title)
        if files:
            return cls(id=files[0]["id"], client=object_client)
        else:
            return cls.create_new(title, object_client)
