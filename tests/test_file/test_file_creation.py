import uuid
from os.path import abspath, dirname, join

from pygsuite.drive import File


TEST_ID = uuid.uuid4()


def test_file_creation__empty_file(auth_test_clients):
    new_file = File.create(name=f"Empty file {TEST_ID}")
    assert new_file.id is not None
    new_file.delete()


def test_file_creation__starred_file(auth_test_clients):
    new_file = File.create(name=f"Starred file {TEST_ID}", starred=True)
    assert new_file.id is not None
    new_file.delete()


def test_file_creation__specified_mimetype(auth_test_clients):
    new_file = File.create(name=f"Empty text file {TEST_ID}", mimetype="text/plain")
    assert new_file.id is not None
    new_file.delete()


def test_file_creation__specified_google_mimetype(auth_test_clients):
    from pygsuite.enums import MimeType

    new_file = File.create(name=f"Empty Spreadsheet {TEST_ID}", mimetype=MimeType.SHEETS)
    assert new_file.id is not None
    new_file.delete()


def test_file_creation__from_bytes(auth_test_clients):
    from io import BytesIO
    import requests

    response = requests.get(
        "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg"
    )
    bytes = BytesIO(response.content)

    new_file = File.create(
        name=f"Test image file {TEST_ID}",
        mimetype="image/svg+xml",
        media_body=bytes,
    )
    assert new_file.id is not None
    new_file.delete()


def test_file_creation__custom_body(auth_test_clients):
    custom_body = {"description": "minimal test of custom body"}
    new_file = File.create(
        name=f"Custom body test {TEST_ID}",
        mimetype="text/plain",
        extra_body=custom_body,
    )
    assert new_file.id is not None
    new_file.delete()


def test_file_upload__from_local_file(auth_test_clients):
    upload_file = join(dirname(dirname(abspath(__file__))), "test_file", "assets", "test.txt")
    print(upload_file)
    new_file = File.upload(
        filepath=upload_file,
        name=f"Test test upload {TEST_ID}",
        mimetype="text/plain",
    )
    assert new_file.id is not None
    new_file.delete()


def test_file_upload__from_local_file__with_conversion(auth_test_clients):
    from pygsuite.enums import GoogleDocFormat
    upload_file = join(dirname(dirname(abspath(__file__))), "test_file", "assets", "test data.xlsx")
    new_file = File.upload(
        filepath=upload_file,
        name=f"Test Excel upload {TEST_ID}",
        convert_to=GoogleDocFormat.SHEETS,
    )
    assert new_file.id is not None
    new_file.delete()
