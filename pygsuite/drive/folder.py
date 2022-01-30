from typing import List, Optional, Union

from googleapiclient.discovery import Resource

from pygsuite import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.drive.file import File
from pygsuite.drive.query import Operator, QueryString, QueryStringGroup, QueryTerm
from pygsuite.enums import GoogleMimeType


class Folder:
    """Base class for a Google Drive Folder"""

    mimetype = GoogleMimeType.FOLDER

    def __init__(self, id: str = None, client: Optional[Resource] = None):

        self.id = parse_id(id) if id else None
        self.client = client or Clients.drive_client

    @classmethod
    def create(
        cls,
        name: str,
        parent_folder_ids: Optional[List[str]] = None,
        drive_client: Optional[Resource] = None,
    ):
        """Create a new folder with a specified location.

        Args:
            name (str): Name of the folder to create.
            parent_folder_ids (List[str]): The IDs of the parent folders which contain the folder.
                If not specified as part of a create request, the file will be placed directly in the user's My Drive folder.
            drive_client (Resource): client connection to the Drive API used to create folder.
        """

        # establish a client
        drive_client = drive_client or Clients.drive_client_v3

        # create request body
        body = {"name": name, "mimeType": str(cls.mimetype)}

        if parent_folder_ids:
            body["parents"] = parent_folder_ids

        new_folder = drive_client.files().create(
            body=body,
            fields="id",
        )

        return Folder(id=new_folder.get("id"), client=drive_client)

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
        print(f"RESPONSE:\n{response}")

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
