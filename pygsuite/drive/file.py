import os
from typing import Optional, Union

from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload

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
    def upload(
        cls,
        filepath: str,
        name: Optional[str] = None,
        convert_to: Optional[Union[str, GoogleDocFormat]] = None,
        client: Optional[Resource] = None,
    ):
        """Method to upload a local file to Google Drive.

        Args:
            filepath (str): Filepath of the file to upload
            name (str): Name of the file in Google Drive once uploaded
            convert (bool): Convert the upload file into a Google App file (e.g. CSV -> Google Sheet)
        """
        # establish a client
        client = client or Clients.drive_client

        # get upload file size
        filesize = os.path.getsize(filepath)
        if filesize > DRIVE_FILE_MAX_SINGLE_UPLOAD_SIZE:
            # TODO: do something for resumable uploads
            resumable = True

        # get filename and extension
        _, extension = os.path.splitext(filepath)

        # name of the file in Drive
        name = name if name else os.path.basename(filepath)
        file_metadata = {"name": name}

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
                file_metadata["mimeType"] = mimetype
            except Exception as e:
                raise ValueError(
                    f"File extension {extension.lower()} is not supported with the Google Document type {convert_to.value}"
                ) from e
        else:
            mimetype = None

        media = MediaFileUpload(filename=filepath, mimetype=mimetype, chunksize=-1)

        file = client.files().create(
            body=file_metadata,
            media_body=media,
            fields="id",
        ).execute()

        return File(id=file.get("id"), client=client)
