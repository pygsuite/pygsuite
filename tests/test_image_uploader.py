import base64
from json import loads
from os import environ

import requests

from pygsuite import ImageUploader


def get_test_image():
    return base64.b64decode(environ["TEST_IMAGE"].encode("utf-8"))


def test_from_string():
    assert environ["TEST_BUCKET"] and environ["TEST_GCS_ACCOUNT"]
    uploader = ImageUploader(
        bucket=environ["TEST_BUCKET"], account_info=environ["TEST_GCS_ACCOUNT"]
    )
    url = uploader.signed_url_from_string(get_test_image(), "png")
    fetch = requests.get(url)
    assert fetch.status_code == 200


def test_from_dict():
    uploader = ImageUploader(
        bucket=environ["TEST_BUCKET"], account_info=loads(environ["TEST_GCS_ACCOUNT"])
    )
