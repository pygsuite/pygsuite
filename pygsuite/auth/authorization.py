from __future__ import print_function

from os.path import dirname, join
import os.path
import pickle
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build

from pygsuite.utility.decorators import lazy_property

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]

SHEETS_VERSION = "v4"
DOCS_VERSION = "v1"
SLIDES_VERSION = "v1"
DRIVE_VERSION = "v2"


def json_str_to_oauth(token_str: str) -> Credentials:
    """Convert a JSON-like string into a Google OAuth `Credentials` object.

    Args:
        token_str (str): A JSON-like string containing Google authentication information.

    Returns a `Credentials` object.
    """
    import json

    cred_dict = json.loads(token_str)
    return Credentials(**cred_dict)


def get_oauth_credential(credential_string: str) -> Credentials:
    """Convert a JSON-like string into a Google OAuth `Credentials` object,
    and refresh the credentials if they are expired and contain a refresh token.
    Raises a `ValueError` if invalid credentials cannot be refreshed.

    Args:
        credential_string (str): A JSON-like string containing Google authentication information.

    Returns a valid `Credentials` object.
    """
    creds = json_str_to_oauth(credential_string)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            return creds
        raise ValueError(
            "Stored user token is no longer valid and no refresh token! Must be regenerated"
        )
    return creds


class _Clients(object):
    """Base client object for authorization to all Google APIs.
    This object contains methods to authorize local files, `Credentials` objects, and more.
    """

    def __init__(self):
        """Class constructor"""
        self.cred_path = None
        self.cred_text = None
        self.auth = None

    def validate(self):
        """Method to verify authorization has been obtained.
        Raises a `ValueError` if no `Credentials` object exists in `self.auth`.
        """
        if not self.auth:
            raise ValueError("Need to provide credential path or credential text or auth object.")

    def auth_default(self, project: Optional[str] = None):
        """Gets the default credentials for the current environment.
        More information in [Google's default auth documentation](
            https://google-auth.readthedocs.io/en/master/reference/google.auth.html#google.auth.default
        )

        Args:
            project (Optional[str]): The project ID.

        Sets the client auth to the default credentials fetched from Google.
        """
        import google.auth

        self.auth, project_id = google.auth.default(quota_project_id=project)

    def create_client_file_from_string(self) -> Flow:
        """Creates a OAuth 2.0 Authorization Flow object from a credential string if provided.

        Returns a constructed `Flow` object with credential information from credential string.
        """
        from tempfile import TemporaryDirectory
        import os

        with TemporaryDirectory() as temppath:
            with open(os.path.join(temppath, "writer-key.json"), "w") as keyfile:
                keyfile.write(self.cred_text)
            flow = InstalledAppFlow.from_client_secrets_file(keyfile.name, SCOPES)
        return flow

    def authorize(self, auth: Credentials, project: Optional[str] = None):
        """Sets the credentials for the current environment to a given `Credentials` object.

        Args:
            auth (Credentials): A valid `google.oauth2.credentials.Credentials` object.
            project (Optional[str]): The project ID, not currently used.
        """
        self.auth = auth

    def authorize_string(self, auth_string: str):
        """Sets the credentials for the current environment based on a JSON-like credentials string.

        Args:
            auth_string (str): A JSON-like string containing credentials information to be authenticated.
        """
        self.auth = get_oauth_credential(auth_string)

    def local_file_auth(self, filepath: str):
        """Sets the credentials for the current environment based on a local file with credentials.

        Args:
            filepath (str): Filepath to the credentials file.
        """
        directory = dirname(filepath)
        pickle_path = join(directory, "cache.pickle")
        creds = None
        if os.path.exists(pickle_path):
            with open(pickle_path, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(filepath, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(pickle_path, "wb") as token:
                pickle.dump(creds, token)
        self.auth = creds

    @lazy_property
    def docs_client(self):
        """Google Docs client"""
        self.validate()
        return build("docs", DOCS_VERSION, credentials=self.auth)

    @lazy_property
    def sheets_client(self):
        """Google Sheets client"""
        self.validate()
        return build("sheets", SHEETS_VERSION, credentials=self.auth)

    @lazy_property
    def slides_client(self):
        """Google Slides client"""
        self.validate()
        return build("slides", SLIDES_VERSION, credentials=self.auth)

    @lazy_property
    def _local_sheets_client(self):
        return build("sheets", SHEETS_VERSION, credentials=self.auth)

    @lazy_property
    def local_docs_client(self):
        return build("docs", DOCS_VERSION, credentials=self.auth)

    @lazy_property
    def _local_slides_client(self):
        return build("slides", SLIDES_VERSION, credentials=self.auth)

    @lazy_property
    def drive_client(self):
        """Google Drive client (API v3)"""
        return self.drive_client_v3

    @lazy_property
    def drive_client_v2(self):
        """Google Drive client (API v2)"""
        self.validate()
        return build("drive", DRIVE_VERSION, credentials=self.auth)

    @lazy_property
    def drive_client_v3(self):
        """Google Drive client (API v3)"""
        self.validate()
        return build("drive", "v3", credentials=self.auth)


Clients = _Clients()
