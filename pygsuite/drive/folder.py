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
        self.client: Resource = client or Clients.drive_client

        DriveObject.__init__(self, id=id, client=self.client)

    def get_files(
        self,
        extra_conditions: Optional[Union[QueryString, QueryStringGroup]] = None,
        support_all_drives: bool = True,
    ) -> List[File]:
        """The files in a given folder. If no folder ID is given in the instance,
        a recursive search is performed from the Drive root.

        Args:
            extra_conditions (Union[QueryString, QueryStringGroup]): Any additional queries to pass to the files search.
            support_all_drives (bool): Whether the requesting application supports both My Drives and shared drives.

        Returns a list of any Files found.
        """
        query_components: List[Union[QueryString, QueryStringGroup]] = []

        if self.id:
            query_components.append(QueryString(QueryTerm.PARENTS, Operator.IN, self.id))

        if extra_conditions:
            query_components.append(extra_conditions)

        query = QueryStringGroup(query_components).formatted if query_components else None

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
