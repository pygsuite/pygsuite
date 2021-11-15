from typing import Optional

from googleapiclient.discovery import Resource

from pygsuite import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.drive.file import File
from pygsuite.drive.query import Operator, QueryString, QueryTerm


class Folder:
    """Base class for a Google Drive Folder"""

    def __init__(self, id: str = None, client: Optional[Resource] = None):

        self.id = parse_id(id) if id else None
        self.client = client or Clients.drive_client

    @property
    def files(self):

        files = []
        page_token = None

        query = QueryString(QueryTerm.PARENTS, Operator.IN, self.id).formatted

        response = (
            self.client.files()
            .list(
                q=query,
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
            ).execute()
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
                ).execute()
            )

            for file in response.get("files", []):
                files.append(File(file.get("id")))

            page_token = response.get("nextPageToken", None)

        return files
