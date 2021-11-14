from io import BytesIO
import os
from typing import Optional, Union

from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

from pygsuite.auth.authorization import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.constants import DRIVE_FILE_MAX_SINGLE_UPLOAD_SIZE
from pygsuite.enums import GoogleDocFormat


FILE_MIME_TYPE_MAP = {
    GoogleDocFormat.DOCS: {
        ".html": "text/html",
        ".txt": "text/plain",
        ".rtf": "application/rtf",
        ".odt": "application/vnd.oasis.opendocument.text",
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".doc": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".epub": "application/epub+zip",
    },
    GoogleDocFormat.SHEETS: {
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".ods": "application/x-vnd.oasis.opendocument.spreadsheet",
        ".pdf": "application/pdf",
        ".csv": "text/csv",
        ".tsv": "text/tab-separated-values",
    },
    GoogleDocFormat.DRAWINGS: {
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".png": "image/png",
        ".svg": "image/svg+xml",
        ".pdf": "application/pdf",
    },
    GoogleDocFormat.SLIDES: {
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".ppt": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".odp": "application/vnd.oasis.opendocument.presentation",
        ".pdf": "application/pdf",
        ".txt": "text/plain",
    },
    GoogleDocFormat.SCRIPTS: {
        ".json": "application/vnd.google-apps.script+json",
    },
}


class File:
    """Base class for a Google Drive File"""

    def __init__(self, id: str = None, client: Optional[Resource] = None):

        self.id = parse_id(id) if id else None
        self.client = client or Clients.drive_client

    @classmethod
    def create(
        cls,
        name: Optional[str] = None,
        mimetype: Optional[str] = None,
        body: Optional[dict] = None,
        media_body: Optional[Union[BytesIO, MediaFileUpload, MediaIoBaseUpload]] = None,
        client: Optional[Resource] = None,
    ):
        """Create a new file in Google Drive.

        Args:
            name (str): Name of the file.
            mimetype (str): Specified type of the file to create.
            body (dict): Request body, if not provided, one is created with `name` and `mimetype` params.
            media_body (BytesIO, MediaFileUpload, MediaIoBaseUpload): Content for the file.
            client (Resource): client connection to the Drive API.
        """

        # establish a client
        client = client or Clients.drive_client

        # create request body
        body = {"name": name, "mimeType": mimetype} if not body else body

        # handle media conversion for bytes-like objects
        if isinstance(media_body, BytesIO):
            # if a mimetype is not provided, find best match
            if not mimetype:
                import magic
                mimetype = magic.from_buffer(media_body.read())

            media_body = MediaIoBaseUpload(fd=media_body, mimetype=mimetype)

        # execute files.create request and return File object
        file = (
            client.files()
            .create(
                body=body,
                media_body=media_body,
                fields="id",
            )
            .execute()
        )

        return File(id=file.get("id"), client=client)

    @classmethod
    def upload(
        cls,
        filepath: str,
        name: Optional[str] = None,
        mimetype: Optional[str] = None,
        convert_to: Optional[Union[str, GoogleDocFormat]] = None,
        client: Optional[Resource] = None,
    ):
        """Method to upload a local file to Google Drive.

        Args:
            filepath (str): Filepath of the file to upload.
            name (str): Name of the file in Google Drive once uploaded.
            mimetype (str): Specified type of the file to create. mimetype is automatically determined if not specified.
            convert_to (str, GoogleDocFormat): Convert the upload file into a Google App file (e.g. CSV -> Google Sheet)
            client (Resource): client connection to the Drive API.
        """
        # establish a client
        client = client or Clients.drive_client

        # get upload file size
        filesize = os.path.getsize(filepath)

        # establish if the upload should be resumable
        # TODO: expand upon this and determine how this should work for users
        if filesize > DRIVE_FILE_MAX_SINGLE_UPLOAD_SIZE:
            resumable = True
        else:
            resumable = False

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
            client=client,
        )

        return file

    def delete(self):
        """Permanently deletes a file owned by the user without moving it to the trash."""

        self.client.files().delete(fileId=self.id).execute()
