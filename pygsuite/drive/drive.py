import warnings
from typing import Optional, Union

from pygsuite import Clients
from pygsuite.drive.folder import Folder
from pygsuite.drive.query import Operator, QueryString, QueryStringGroup, QueryTerm
from pygsuite.enums import MimeType


DRIVE_V3_API_URL = "https://www.googleapis.com/drive/v3/files"


def default_callback(request_id, response, exception):
    if exception:
        # Handle error
        raise ValueError(exception)


class Drive:
    """Due for deprecation, please use File and Folder to search and create objects."""

    def __init__(self, client=None):
        client = client or Clients.drive_client_v3
        self.service = client

        # warn users about deprecation
        warnings.warn((
            "This object and its methods will be deprecated soon."
            "Please consider using a drive.File or drive.Folder object instead"
        ), DeprecationWarning)

    def _find_files(self, type: MimeType, name: Optional[str] = None):
        q = f'mimeType="{type}"'
        if name:
            q += f' and name = "{name}"'
        base = self.service.files().list(q=q).execute()
        files = base.get("files")
        page_token = base.get("nextPageToken")
        while page_token is not None:
            base = self.service.files().list(q=q, page_token=page_token).execute()
            files += base.get("files")
            page_token = base.get("nextPageToken")
        return files

    def find_files(
        self,
        folder_id: Optional[str] = None,
        name: Optional[str] = None,
        exact_match: bool = True,
        type: Optional[Union[MimeType, str]] = None,
        extra_conditions: Optional[Union[QueryString, QueryStringGroup]] = None,
        support_all_drives: bool = False,
    ):
        """Find matching files given certain criteria.

        Args:
            folder_id (str): The folder ID to search within. If none is provided, a recursive search of all folders is performed.
            name (str): The case-sensitive name of the file to search for.
            exact_match (bool): Whether to only match the given name exactly, or return any name containing the string.
            type (Union[MimeType, str]): A specific Google Docs type to match.
            extra_conditions (Union[QueryString, QueryStringGroup]): Any additional queries to pass to the files search.
            support_all_drives (bool): Whether the requesting application supports both My Drives and shared drives.
        """
        query = None

        # name match query
        if name:
            operator = Operator.EQUAL if exact_match else Operator.CONTAINS
            name_query = QueryString(QueryTerm.NAME, operator, name)
            query = name_query

        # optional type query
        if type:
            mimetype = str(type) if isinstance(type, MimeType) else type
            type_query = QueryString(QueryTerm.MIMETYPE, Operator.EQUAL, mimetype)
            query = QueryStringGroup([query, type_query]) if query else type_query

        # optional auxillary query
        if extra_conditions:
            query = QueryStringGroup([query, extra_conditions]) if query else extra_conditions

        folder = Folder(id=folder_id, client=self.service)
        files = folder.get_files(extra_conditions=query, support_all_drives=support_all_drives)

        return files

    def copy_file(self, file_id, title: str, folder_id: str):
        body = {"name": title, "parents": [folder_id]}
        response = self.service.files().copy(fileId=file_id, body=body).execute()
        return response
