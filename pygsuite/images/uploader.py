import datetime
import json
from typing import Union, Dict, Tuple
from uuid import uuid4

from google.cloud.storage import Client

_SERVICE_ACCOUNT_TYPE = "service_account"


def generate_download_signed_url_v4(bucket, blob_name: str, timeout: int = 15):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=timeout),
        # Allow GET requests using this URL.
        method="GET",
    )
    return url


class ImageUploader:
    def __init__(self, bucket: str, account_info: Union[Client, str, Dict], timeout: int = 15):
        self.account_info = account_info
        self.timeout = timeout
        self._client, self._project = (
            (account_info, None)
            if isinstance(account_info, Client)
            else self._generate_client(account_info)
        )

        self.client = Client(credentials=self._client, project=self._project)
        self.bucket = self.client.bucket(bucket)

    def _generate_client(self, info: Union[Dict, str]) -> Tuple[Client, str]:
        if not isinstance(info, dict):
            info = json.loads(info)

        # The type key should indicate that the file is either a service account
        # credentials file or an authorized user credentials file.
        credential_type = info.get("type")
        if credential_type != _SERVICE_ACCOUNT_TYPE:
            raise ValueError(
                f'Invalid credential type "{credential_type}". Generating signed URLs requires a service account with appropriate permissions.'
            )

        from google.oauth2 import service_account

        return service_account.Credentials.from_service_account_info(info), info.get("project_id")

    def _get_signed_url(self, obj: str):
        return generate_download_signed_url_v4(self.bucket, obj, self.timeout)

    def signed_url_from_file(self, path: str):
        temp_file_name = str(uuid4())
        blob = self.bucket.blob(temp_file_name)
        blob.upload_from_filename(path)
        return self._get_signed_url(temp_file_name)

    def signed_url_from_string(self, string, type: str = "png"):
        temp_file_name = str(uuid4())
        blob = self.bucket.blob(temp_file_name)
        blob.upload_from_string(string, content_type=f"application/{type}")
        return self._get_signed_url(temp_file_name)
