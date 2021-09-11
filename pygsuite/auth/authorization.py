from __future__ import print_function

from os.path import dirname, join
import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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
    import json

    cred_dict = json.loads(token_str)
    return Credentials(**cred_dict)


def get_oauth_credential(credential_string: str) -> Credentials:
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
    def __init__(self):
        self.cred_path = None
        self.cred_text = None
        self.auth = None

    def validate(self):
        if not self.auth:
            raise ValueError("Need to provide credential path or credential text or auth object.")

    def auth_default(self, project: str = None):
        import google.auth

        self.auth, project_id = google.auth.default(quota_project_id=project)

    def create_client_file_from_string(self):
        from tempfile import TemporaryDirectory
        import os

        with TemporaryDirectory() as temppath:
            with open(os.path.join(temppath, "writer-key.json"), "w") as keyfile:
                keyfile.write(self.cred_text)
            flow = InstalledAppFlow.from_client_secrets_file(keyfile.name, SCOPES)
        return flow

    def authorize(self, auth, project=None):
        self.auth = auth

    def authorize_string(self, auth_string: str):
        self.auth = get_oauth_credential(auth_string)

    def local_file_auth(self, path: str):
        directory = dirname(path)
        pickle_path = join(directory, "cache.pickle")
        creds = None
        if os.path.exists(pickle_path):
            with open(pickle_path, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(pickle_path, "wb") as token:
                pickle.dump(creds, token)
        self.auth = creds

    @lazy_property
    def docs_client(self):
        self.validate()
        return build("docs", DOCS_VERSION, credentials=self.auth)

    @lazy_property
    def sheets_client(self):
        self.validate()
        return build("sheets", SHEETS_VERSION, credentials=self.auth)

    @lazy_property
    def slides_client(self):
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
        return self.drive_client_v3

    @lazy_property
    def drive_client_v2(self):
        self.validate()
        return build("drive", "v2", credentials=self.auth)

    @lazy_property
    def drive_client_v3(self):
        self.validate()
        return build("drive", "v3", credentials=self.auth)


Clients = _Clients()
