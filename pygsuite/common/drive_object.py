from typing import List, Optional

from pygsuite import Clients
from pygsuite.common.comment import Comment
from pygsuite.enums import FileTypes, PermissionType
from pygsuite.utility.decorators import lazy_property


def default_callback(request_id, response, exception):
    if exception:
        # Handle error
        raise ValueError(exception)


class DriveObject:
    file_type: FileTypes = FileTypes.UNKNOWN

    def __init__(
        self,
        id,
        client,
    ):
        self.id = id
        self.client = client

    @property
    def comments(self) -> List[Comment]:
        return [
            Comment(item)
            for item in self.drive_client.comments().list(fileId=self.id).execute().get("items", [])
        ]

    @lazy_property
    def drive_client(self):
        return Clients.drive_client_v2

    @lazy_property
    def drive_client_3(self):
        return Clients.drive_client_v3

    @classmethod
    def create_new(cls, title: str, client=None):
        raise NotImplementedError

    @classmethod
    def get_safe(cls, title: str, drive_client=None, object_client=None):
        from pygsuite.drive import Drive

        file_client = drive_client or Clients.drive_client_v3
        files = Drive(client=file_client).find_files(cls.file_type, name=title)
        if files:
            return cls(id=files[0]["id"], client=object_client)
        else:
            return cls.create_new(title, object_client)

    def share(
        self,
        role: PermissionType,
        user: Optional[str] = None,
        group: Optional[str] = None,
        domain: Optional[str] = None,
        everyone: bool = False,
    ):
        """Share the object with a provided permission with a user, group, domain, or everyone."""
        permissions: List[dict] = []
        role = PermissionType(role)
        if user:
            permissions.append({"role": role.value, "type": "user", "emailAddress": user})
        if group:
            permissions.append({"role": role.value, "type": "group", "emailAddress": group})
        if domain:
            permissions.append({"role": role.value, "type": "domain", "domain": domain})
        if everyone:
            permissions.append({"role": role.value, "type": "everyone"})
        for permission in permissions:
            self.drive_client_3.permissions().create(
                fileId=self.id, body=permission, supportsAllDrives=True
            ).execute()
