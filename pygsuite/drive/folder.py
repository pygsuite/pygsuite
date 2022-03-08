from typing import List, Optional, Union

from googleapiclient.discovery import Resource

from pygsuite import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.drive.drive_object import DriveObject
from pygsuite.drive.file import File
from pygsuite.drive.query import Operator, QueryString, QueryStringGroup, QueryTerm
from pygsuite.enums import MimeType
from pygsuite.utility.requests import execute_paginated_command


class Folder(DriveObject):
    """Base class for a Google Drive Folder"""

    _mimetype = MimeType.FOLDER
    _base_url = "https://drive.google.com/drive/folders/{}"

    def __init__(self, id: str = None, client: Optional[Resource] = None):

        self.id = parse_id(id) if id else None
        self.client = client or Clients.drive_client

        DriveObject.__init__(self, id=id, client=self.client)

    def get_files(
        self,
        extra_conditions: Optional[Union[QueryString, QueryStringGroup]] = None,
        support_all_drives: bool = False,
    ) -> List[File]:
        """The files in a given folder. If no folder ID is given in the instance,
        a recursive search is performed from the Drive root.

        Args:
            extra_conditions (Union[QueryString, QueryStringGroup]): Any additional queries to pass to the files search.
            support_all_drives (bool): Whether the requesting application supports both My Drives and shared drives.

        Returns a list of any Files found.
        """
        query = None

        if self.id:
            query = QueryString(QueryTerm.PARENTS, Operator.IN, self.id)

        if extra_conditions:
            query = (
                QueryStringGroup([query, extra_conditions])
                if query is not None
                else extra_conditions
            )

        query = query.formatted if query else query

        files = execute_paginated_command(
            client=self.client.files(),
            method="list",
            fetch_field="files",
            q=query,
            spaces="drive",
            fields="nextPageToken, files(id, name)",
            supportsAllDrives=support_all_drives,
            includeItemsFromAllDrives=support_all_drives,
        )

        return [File(file.get("id")) for file in files]
