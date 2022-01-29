from io import BytesIO
import logging
import os
from typing import List, Optional, Union

from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

from pygsuite.auth.authorization import Clients
from pygsuite.common.comment import Comment
from pygsuite.common.parsing import parse_id
from pygsuite.constants import DRIVE_FILE_MAX_SINGLE_UPLOAD_SIZE, FILE_MIME_TYPE_MAP
from pygsuite.drive.query import Operator, QueryString, QueryStringGroup, QueryTerm
from pygsuite.enums import GoogleDocFormat, PermissionType, GoogleMimeTypes
from pygsuite.utility.decorators import lazy_property


class File:
    """Base class for a Google Drive File"""

    def __init__(self, id: str = None, client: Optional[Resource] = None):

        self.id = parse_id(id) if id else None
        self.client = client

        # metadata cache
        self._metadata = None

    @lazy_property
    def drive_client(self):
        return Clients.drive_client_v3

    @classmethod
    def create(
        cls,
        name: Optional[str] = None,
        mimetype: Optional[Union[str, GoogleMimeTypes]] = None,
        body: Optional[dict] = None,
        media_body: Optional[Union[BytesIO, MediaFileUpload, MediaIoBaseUpload]] = None,
        drive_client: Optional[Resource] = None,
        object_client: Optional[Resource] = None,
    ):
        """Create a new file in Google Drive.

        Args:
            name (str): Name of the file.
            mimetype (str): Specified type of the file to create.
            body (dict): Request body, if not provided, one is created with `name` and `mimetype` params.
            media_body (BytesIO, MediaFileUpload, MediaIoBaseUpload): Content for the file.
            drive_client (Resource): client connection to the Drive API used to create file.
            object_client (Resource): optional domain client (e.g. SHEETS client) used by the created object.
        """

        # establish a client
        drive_client = drive_client or Clients.drive_client_v3

        # handle Google mimetypes
        mimetype = str(mimetype) if isinstance(mimetype, GoogleMimeTypes) else mimetype

        # create request body
        body = {"name": name, "mimeType": mimetype} if not body else body

        # handle media conversion for bytes-like objects
        if isinstance(media_body, BytesIO):
            # if a mimetype is not provided, find best match
            if not mimetype:
                logging.warning("No mimetype specified, attempting to determine one.")

                import magic

                mimetype = magic.from_buffer(media_body.read())

            media_body = MediaIoBaseUpload(fd=media_body, mimetype=mimetype)

        # execute files.create request and return File object
        file = (
            drive_client.files()
            .create(
                body=body,
                media_body=media_body,
                fields="id",
            )
            .execute()
        )
        print(f"ID: {file.get('id')}")

        return File(id=file.get("id"), client=object_client)

    @classmethod
    def upload(
        cls,
        filepath: str,
        name: Optional[str] = None,
        mimetype: Optional[str] = None,
        convert_to: Optional[Union[str, GoogleDocFormat]] = None,
        drive_client: Optional[Resource] = None,
        object_client: Optional[Resource] = None,
    ):
        """Method to upload a local file to Google Drive.

        Args:
            filepath (str): Filepath of the file to upload.
            name (str): Name of the file in Google Drive once uploaded.
            mimetype (str): Specified type of the file to create. mimetype is automatically determined if not specified.
            convert_to (str, GoogleDocFormat): Convert the upload file into a Google App file (e.g. CSV -> Google Sheet)
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

        media_body = MediaFileUpload(
            filename=filepath, mimetype=mimetype, chunksize=-1, resumable=resumable
        )

        file = cls.create(
            name=name,
            mimetype=mimetype,
            media_body=media_body,
            drive_client=drive_client,
            client=object_client,
        )

        return file

    @classmethod
    def get_safe(
        cls,
        title: str,
        exact_match: bool = True,
        type: Optional[Union[GoogleMimeTypes, str]] = None,
        extra_conditions: Optional[Union[QueryString, QueryStringGroup]] = None,
        drive_client: Optional[Resource] = None,
        object_client: Optional[Resource] = None,
    ):
        """Get a file or create one if not found

        Args:
            title (str): The case-sensitive title of the file to search for.
            exact_match (bool): Whether to only match the given title exactly, or return any title containing the string.
            type (Union[GoogleMimeTypes, str]): A specific Google Docs type to match.
            extra_conditions (Union[QueryString, QueryStringGroup]): Any additional queries to pass to the files search.
            drive_client (Resource): client connection to the Drive API used to create file.
            object_client (Resource): optional domain client (e.g. SHEETS client) used by the created object.

        Returns:
            An instantiated File object, or specific Google Docs type object, such as Spreadsheet, Presentation, or Document.
        """
        # establish a client
        drive_client = drive_client or Clients.drive_client_v3

        # title match query
        operator = Operator.EQUAL if exact_match else Operator.CONTAINS
        title_query = QueryString(QueryTerm.NAME, operator, title)
        query = title_query

        # optional type query
        if type:
            mimetype = str(type) if isinstance(type, GoogleMimeTypes) else type
            type_query = QueryString(QueryTerm.MIMETYPE, Operator.EQUAL, mimetype)
            query = QueryStringGroup([query, type_query])

        # optional auxillary query
        if extra_conditions:
            query = QueryStringGroup([query, extra_conditions])

        # we are not handling multiple pages of matches here because
        # we only return the first match any way
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
        print(f"QUERY RESPONSE:\n{response}")

        files = response.get("files", [])
        if files:
            # TODO: better method for determining *best* match from a set of matches
            return cls(files[0].get("id"), object_client)
        else:
            # TODO: do we want to raise an exception or add helpful logging here?
            return None

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
        if fields is None:
            fields = ["id", "kind", "name", "mimeType"]

        metadata = {}

        # see if we have cached the file metadata already
        if ignore_cache is False:
            try:
                for field in fields:
                    metadata[field] = self._metadata[field]

                return metadata

            # if we cannot find a field, we need to fetch the metadata again
            except KeyError:
                pass

        self._metadata = (
            self.client.files().get(
                fileId=self.id,
                fields=f"{', '.join(fields)}",
            )
        ).execute()

        for field in fields:
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
    def comments(self) -> List[Comment]:

        return [
            Comment(item)
            for item in self.drive_client.comments().list(fileId=self.id).execute().get("items", [])
        ]

    def share(
        self,
        role: PermissionType,
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
            self.drive_client.permissions().create(
                fileId=self.id, body=permission, supportsAllDrives=True
            ).execute()

    def delete(self):
        """Permanently deletes a file owned by the user without moving it to the trash."""

        self.drive_client.files().delete(fileId=self.id).execute()
