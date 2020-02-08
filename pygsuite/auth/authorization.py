from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from pygsuite.utility.decorators import lazy_property

SCOPES = ['https://www.googleapis.com/auth/documents',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/presentations',
          'https://www.googleapis.com/auth/drive']


class Clients(object):
    def __init__(self, cred_path: str = None, cred_text: str = None):
        self.cred_path = cred_path
        self.cred_text = cred_text
        if not self.cred_path or self.cred_text:
            raise ValueError(f'Need to provide credential path or credential text')

    def create_client_file_from_string(self):
        from tempfile import TemporaryDirectory
        import os
        with TemporaryDirectory() as temppath:
            with open(os.path.join(temppath, "writer-key.json"), "w") as keyfile:
                keyfile.write(self.cred_text)
            flow = InstalledAppFlow.from_client_secrets_file(
                keyfile.name, SCOPES)
        return flow

    @lazy_property
    def auth(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.cred_path, SCOPES) if self.cred_path else self.create_client_file_from_string()
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    @lazy_property
    def docs_client(self):
        return build('docs', 'v1', credentials=self.auth)

    @lazy_property
    def sheets_client(self):
        return build('sheets', 'v4', credentials=self.auth)

    @lazy_property
    def slides_client(self):
        return build('slides', 'v1', credentials=self.auth)
