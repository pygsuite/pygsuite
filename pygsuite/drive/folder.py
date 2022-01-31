from typing import Optional, Union

from googleapiclient.discovery import Resource

from pygsuite import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.drive.drive_object import DriveObject
from pygsuite.drive.file import File
from pygsuite.drive.query import Operator, QueryString, QueryStringGroup, QueryTerm
from pygsuite.enums import GoogleMimeType


class Folder(DriveObject):
    """Base class for a Google Drive Folder"""

    _mimetype = GoogleMimeType.FOLDER

    def __init__(self, id: str = None, client: Optional[Resource] = None):

        self.id = parse_id(id) if id else None
        self.client = client or Clients.drive_client

        DriveObject.__init__(self, id=id, client=self.client)

    def get_files(
        self,
        extra_conditions: Optional[Union[QueryString, QueryStringGroup]] = None,
        support_all_drives: bool = False,
    ):
        """The files in a given folder. If no folder ID is given in the instance,
        a recursive search is performed from the Drive root.

        Args:
            extra_conditions (Union[QueryString, QueryStringGroup]): Any additional queries to pass to the files search.
            support_all_drives (bool): Whether the requesting application supports both My Drives and shared drives.
        """
        query = None
        files = []
        page_token = None

        if self.id:
            query = QueryString(QueryTerm.PARENTS, Operator.IN, self.id)

        if extra_conditions:
            query = (
                QueryStringGroup([query, extra_conditions])
                if query is not None
                else extra_conditions
            )

        query = query.formatted if query else query

        response = (
            self.client.files()
            .list(
                q=query,
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
                supportsAllDrives=support_all_drives,
                includeItemsFromAllDrives=support_all_drives,
            )
            .execute()
        )

        for file in response.get("files", []):
            files.append(File(file.get("id")))

        page_token = response.get("nextPageToken", None)

        while page_token is not None:
            response = (
                self.client.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                    supportsAllDrives=support_all_drives,
                    includeItemsFromAllDrives=support_all_drives,
                )
                .execute()
            )

            for file in response.get("files", []):
                files.append(File(file.get("id")))

            page_token = response.get("nextPageToken", None)

        return files
