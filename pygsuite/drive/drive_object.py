from io import BytesIO
import logging
import os
from typing import List, Optional, Union

import filetype
from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

from pygsuite.auth.authorization import Clients
from pygsuite.common.comment import Comment
from pygsuite.common.parsing import parse_id
from pygsuite.constants import DRIVE_FILE_MAX_SINGLE_UPLOAD_SIZE, FILE_MIME_TYPE_MAP
from pygsuite.drive.query import Connector, Operator, QueryString, QueryStringGroup, QueryTerm
from pygsuite.enums import GoogleDocFormat, PermissionType, MimeType
from pygsuite.utility.decorators import lazy_property


_logger = logging.getLogger(__name__)


class DriveObject:
    """Base class for a Google Drive Object

    Includes common, core functionality including creation, manipulation, deletion, and more.
    Other GSuite objects are derived from this class, including:

    - File
    - Folder
    - Spreadsheet
    - Presentation
    - Document
    """

    _mimetype = MimeType.UNKNOWN
    _base_url = "https://drive.google.com/file/d/{}/view"

    def __init__(self, id: str = None, client: Optional[Resource] = None):

        self.id = parse_id(id) if id else None
        # object-specific client
        self.client = client

        # metadata cache
        self._metadata = None

    @lazy_property
    def _drive_client(self):
        """Google Drive API client used for file manipulations"""
        return Clients.drive_client_v3

    @classmethod
    def _create(
        cls,
        name: Optional[str] = None,
        parent_folder_ids: Optional[List[str]] = None,
        mimetype: Optional[Union[str, MimeType]] = None,
        media_body: Optional[Union[BytesIO, MediaFileUpload, MediaIoBaseUpload]] = None,
        starred: bool = False,
        extra_body: Optional[dict] = None,
        drive_client: Optional[Resource] = None,
        object_client: Optional[Resource] = None,
        **kwargs,
    ):
        """Base create method.

        Args:
            name (str): Name of the file.
            parent_folder_ids (List[str]): The IDs of the parent folders which contain the folder.
                If not specified as part of a create request, the file will be placed directly in the user's My Drive folder.
            mimetype (Union[str, MimeType]): Specified type of the file to create.
            media_body (BytesIO, MediaFileUpload, MediaIoBaseUpload): Content for the file.
            starred (bool): Whether the user has starred the file.
            extra_body (dict): Extra parameters for the request body.
            drive_client (Resource): client connection to the Drive API used to create file.
            object_client (Resource): optional domain client (e.g. SHEETS client) used by the created object.
        """

        # establish a client
        drive_client = drive_client or Clients.drive_client_v3

        # handle Google mimetypes
        mimetype = str(mimetype) if mimetype is not None else None

        # create request body
        body = {
            "name": name,
            "mimeType": mimetype,
            "parents": parent_folder_ids,
            "starred": starred,
        }

        if extra_body:
            body.update(extra_body)

        # handle media conversion for bytes-like objects
        if isinstance(media_body, BytesIO):
            # if a mimetype is not provided, find best match
            if not mimetype:
                logging.warning("No mimetype specified, attempting to determine one.")
                mimetype = filetype.guess_mime(media_body.read(2048))
                logging.info(f"MimeType found for file: {mimetype}")

            media_body = MediaIoBaseUpload(fd=media_body, mimetype=mimetype)

        # execute files.create request and return File object
        file = (
            drive_client.files()
            .create(
                body=body,
                media_body=media_body,
                fields="id",
                **kwargs,
            )
            .execute()
        )

        return DriveObject(id=file.get("id"), client=object_client)

    @classmethod
    def create(
        cls,
        name: Optional[str] = None,
        parent_folder_ids: Optional[List[str]] = None,
        mimetype: Optional[Union[str, MimeType]] = None,
        media_body: Optional[Union[BytesIO, MediaFileUpload, MediaIoBaseUpload]] = None,
        starred: bool = False,
        extra_body: Optional[dict] = None,
        drive_client: Optional[Resource] = None,
        object_client: Optional[Resource] = None,
        **kwargs,
    ):
        """Create a new Google Drive object (e.g. File, Folder, Spreadsheet, Presentation, Document)

        Args:
            name (str): Name of the file.
            parent_folder_ids (List[str]): The IDs of the parent folders which contain the file.
                If not specified as part of a create request, the file will be placed directly in the user's My Drive folder.
            mimetype (Union[str, MimeType]): Specified type of the file to create.
            media_body (BytesIO, MediaFileUpload, MediaIoBaseUpload): Content for the file.
            starred (bool): Whether the user has starred the file.
            extra_body (dict): Extra parameters for the request body.
            drive_client (Resource): client connection to the Drive API used to create file.
            object_client (Resource): optional domain client (e.g. SHEETS client) used by the created object.

        Returns the newly created pygsuite object.
        """
        drive_client = drive_client or Clients.drive_client_v3
        mimetype = mimetype or cls._mimetype

        new_file = cls._create(
            name=name,
            parent_folder_ids=parent_folder_ids,
            mimetype=str(mimetype),
            media_body=media_body,
            starred=starred,
            extra_body=extra_body,
            drive_client=drive_client,
            **kwargs,
        )
        return cls(id=new_file.id, client=object_client)

    @classmethod
    def upload(
        cls,
        filepath: str,
        name: Optional[str] = None,
        parent_folder_ids: Optional[List[str]] = None,
        mimetype: Optional[Union[str, MimeType]] = None,
        convert_to: Optional[Union[str, GoogleDocFormat]] = None,
        starred: bool = False,
        drive_client: Optional[Resource] = None,
        object_client: Optional[Resource] = None,
        **kwargs,
    ):
        """Method to upload a local file to Google Drive.

        Args:
            filepath (str): Filepath of the file to upload.
            name (str): Name of the file in Google Drive once uploaded.
            parent_folder_ids (List[str]): The IDs of the parent folders which contain the file.
                If not specified as part of a create request, the file will be placed directly in the user's My Drive folder.
            mimetype (Union[str, MimeType]): Specified type of the file to create. mimetype is automatically determined if not specified.
            convert_to (str, GoogleDocFormat): Convert the upload file into a Google App file (e.g. CSV -> Google Sheet)
            starred (bool): Whether the user has starred the file.
            drive_client (Resource): client connection to the Drive API used to create file.
            object_client (Resource): optional domain client (e.g. SHEETS client) used by the created object.
        """
        # establish a client
        drive_client = drive_client or Clients.drive_client_v3

        # get upload file size
        filesize = os.path.getsize(filepath)

        # establish if the upload should be resumable
        # TODO: expand upon this and determine how this should work for users
        resumable = filesize > DRIVE_FILE_MAX_SINGLE_UPLOAD_SIZE

        # get filename and extension
        _, extension = os.path.splitext(filepath)

        # name of the file in Drive
        name = name if name else os.path.basename(filepath)

        # handle MimeType enums
        mimetype = str(mimetype) if mimetype is not None else None

        # first use the given mimetype (which can be None) to specify the upload file's mimetype
        media_body = MediaFileUpload(
            filename=filepath, mimetype=mimetype, chunksize=-1, resumable=resumable
        )

        # next, if converting, determine the mimetype of the Google app to convert to
        if convert_to:
            # try to coerce str into a GoogleDocFormat
            if isinstance(convert_to, str):
                try:
                    convert_to = GoogleDocFormat[convert_to.upper()]
                except Exception as e:
                    raise ValueError(
                        f"For converting to a Google Document, please use one of the following inputs:\n{[item.name for item in GoogleDocFormat]}"
                    ) from e

            # find the corresponding mime type of the extension of the upload file
            try:
                mimetype = FILE_MIME_TYPE_MAP[convert_to][extension.lower()]
            except Exception as e:
                raise ValueError(
                    f"File extension {extension.lower()} is not supported with the Google Document type {convert_to.value}"
                ) from e

        file = cls.create(
            name=name,
            parent_folder_ids=parent_folder_ids,
            mimetype=mimetype,
            media_body=media_body,
            starred=starred,
            drive_client=drive_client,
            object_client=object_client,
            **kwargs,
        )

        return file

    @classmethod
    def get_safe(
        cls,
        name: str,
        exact_match: bool = True,
        parent_folder_ids: Optional[List[str]] = None,
        mimetype: Optional[Union[MimeType, str]] = None,
        extra_conditions: Optional[Union[QueryString, QueryStringGroup]] = None,
        drive_client: Optional[Resource] = None,
        object_client: Optional[Resource] = None,
    ):
        """Get a file or create one if not found

        Args:
            name (str): The case-sensitive name of the file to search for.
            exact_match (bool): Whether to only match the given name exactly, or return any name containing the string.
            parent_folder_ids (List[str]): The IDs of the parent folders which contain the file.
            mimetype (Union[GoogleMimeType, str]): A specific Google Docs type to match.
            extra_conditions (Union[QueryString, QueryStringGroup]): Any additional queries to pass to the files search.
            drive_client (Resource): client connection to the Drive API used to create file.
            object_client (Resource): optional domain client (e.g. SHEETS client) used by the created object.

        Returns:
            An instantiated File object, or specific Google Docs type object, such as Spreadsheet, Presentation, or Document.
        """
        # establish a client
        drive_client = drive_client or Clients.drive_client_v3

        # name match query
        operator = Operator.EQUAL if exact_match else Operator.CONTAINS
        name_query = QueryString(QueryTerm.NAME, operator, name)
        query = name_query

        # optional folder query
        if parent_folder_ids:
            folder_queries = []
            for id in parent_folder_ids:
                folder_query = QueryString(QueryTerm.PARENTS, Operator.IN, id)
                folder_queries.append(folder_query)
            folder_query = QueryStringGroup(folder_queries, [Connector.OR for query in folder_queries[:-1]])

            query = QueryStringGroup([query, folder_query])

        # optional mimetype query
        if mimetype:
            mimetype = str(mimetype)
            type_query = QueryString(QueryTerm.MIMETYPE, Operator.EQUAL, mimetype)
            query = QueryStringGroup([query, type_query])

        # optional auxillary query
        if extra_conditions:
            query = QueryStringGroup([query, extra_conditions])

        # we are not handling multiple pages of matches here because
        # we only return the first match anyway
        response = (
            drive_client.files()
            .list(
                q=query.formatted,
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken=None,
            )
            .execute()
        )

        files = response.get("files", [])
        if files:
            # TODO: better method for determining *best* match from a set of matches
            _logger.info("Matching file found, returning existing file...")
            return cls(files[0].get("id"), object_client)
        else:
            _logger.info("No matching file found, creating file now...")
            return cls.create(
                name=name,
                parent_folder_ids=parent_folder_ids,
                mimetype=mimetype,
                object_client=object_client,
            )

    def copy(self):

        raise NotImplementedError

    def move(
        self,
        destination_folder_ids: List[str],
        current_folder_ids: Optional[List[str]] = None,
    ):
        """Move the file from a current folder to a new folder.
        If no current folder is specified, the current folder ID is derived.

        Args:
            destination_folder_id (str): A list of the folder IDs to move the file to.
            current_folder_id (str): A list of the current folder IDs to remove the file from.
        """
        if not current_folder_ids:
            current_folder_ids = self.fetch_metadata().get("parents")

        response = (
            self._drive_client.files()
            .update(
                fileId=self.id,
                addParents=destination_folder_ids,
                removeParents=current_folder_ids,
                fields="parents",
            )
            .execute()
        )

        return response.get("parents")

    def fetch_metadata(
        self,
        ignore_cache: bool = False,
        fields: Optional[List[str]] = None,
    ) -> dict:
        """Metadata for the file, based on the files.get method.
        Default fields include kind, name, and mimetype. Additional fields available are found here:
        https://googleapis.github.io/google-api-python-client/docs/dyn/drive_v3.files.html#get

        Args:
            ignore_cache (bool): whether to first look at the cached metadata.
            fields (Optional[List[str]]): list of fields to return. Use ["*"] to return all.
        """

        # we cannot use the cache if there is none
        if self._metadata is None:
            ignore_cache = True

        # default fields to fetch, needed by default properties
        _fields = ["id", "kind", "name", "mimeType"]
        if fields:
            _fields.extend(fields)

        metadata = {}

        # see if we have cached the file metadata already
        if ignore_cache is False:
            fetch = False
            for field in _fields:
                try:
                    metadata[field] = self._metadata[field]
                # if we cannot find a field, we need to fetch the metadata again
                except KeyError:
                    fetch = True
                    break
            if not fetch:
                _logger.info("Using cached metadata...")
                return metadata

        self._metadata = (
            self._drive_client.files().get(
                fileId=self.id,
                fields=f"{', '.join(_fields)}",
            )
        ).execute()

        for field in _fields:
            metadata[field] = self._metadata[field]

        return metadata

    @property
    def kind(self):

        return self.fetch_metadata().get("kind")

    @property
    def name(self):

        return self.fetch_metadata().get("name")

    @property
    def mimetype(self):

        return self.fetch_metadata().get("mimeType")

    @property
    def url(self):

        return self._base_url.format(self.id)

    @property
    def comments(self) -> List[Comment]:

        return [
            Comment(item)
            for item in self._drive_client.comments()
            .list(
                fileId=self.id,
                fields=None,
            )
            .execute()
            .get("items", [])
        ]

    def update(self):

        raise NotImplementedError

    def share(
        self,
        role: Union[PermissionType, str],
        user: Optional[str] = None,
        group: Optional[str] = None,
        domain: Optional[str] = None,
        anyone: bool = False,
    ):
        """Share the object with a provided permission with a user, group, domain, or everyone.
        More information on operations by role here:
        https://developers.google.com/drive/api/v3/ref-roles

        Args:
            role (PermissionType): role identifying operations that can be performed.
            user (Optional[str]): a user to share the file with.
            group (Optional[str]): a group to share the file with.
            domain (Optional[str]): a domain for a given permission role.
            anyone (bool): make the file accessible to anyone.
        """

        permissions: List[dict] = []

        # coerce any strings into a PermissionType
        role = PermissionType(role)

        if user:
            permissions.append({"role": role.value, "type": "user", "emailAddress": user})
        if group:
            permissions.append({"role": role.value, "type": "group", "emailAddress": group})
        if domain:
            permissions.append({"role": role.value, "type": "domain", "domain": domain})
        if anyone:
            permissions.append({"role": role.value, "type": "anyone"})
        for permission in permissions:
            self._drive_client.permissions().create(
                fileId=self.id, body=permission, supportsAllDrives=True
            ).execute()

    def download(self):

        raise NotImplementedError

    def delete(self):
        """Permanently deletes a file owned by the user without moving it to the trash."""

        self._drive_client.files().delete(fileId=self.id).execute()
