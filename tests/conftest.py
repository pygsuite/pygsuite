import base64
from json import loads, dumps
from os import environ, path
from uuid import uuid4

from pytest import fixture

from pygsuite import Clients
from pygsuite import ImageUploader

if path.isfile("./test_config.json"):
    with open("./test_config.json") as file:
        config = loads(file.read())
        for key, value in config.items():
            if isinstance(value, dict):
                value = dumps(value)
            environ[key] = value


@fixture(scope="session")
def auth_test_clients():
    from google.oauth2.credentials import Credentials
    from google.oauth2.service_account import Credentials as ServiceCredentials

    token = loads(environ["TEST_AUTH"])
    assert isinstance(token, dict)
    if token.get("type"):
        creds = ServiceCredentials.from_service_account_info(token)
    else:
        creds = Credentials(**token)
    Clients.authorize(auth=creds)


@fixture(scope="session")
def test_folder(auth_test_clients):
    from pygsuite import Folder

    test_dir = Folder.get_safe(name=f"test-{uuid4()}")

    yield test_dir

    test_dir.delete()


@fixture(scope="session")
def test_filled_folder(auth_test_clients):
    from pygsuite import File, Folder
    from pygsuite.enums import MimeType

    filled_folder = Folder.get_safe(name=f"Filled folder {uuid4()}")
    child_text_file = File.get_safe(
        name=f"Child text file {uuid4()}",
        parent_folder_ids=[filled_folder.id],
        mimetype="text/plain",
    )
    child_sheets_file = File.get_safe(
        name=f"Child text file {uuid4()}",
        parent_folder_ids=[filled_folder.id],
        mimetype=MimeType.SHEETS,
    )

    yield filled_folder, child_text_file, child_sheets_file

    child_text_file.delete()
    child_sheets_file.delete()
    filled_folder.delete()


@fixture(scope="session")
def test_text_file(auth_test_clients):
    from pygsuite import File

    test_file = File.get_safe(name=f"test-{uuid4()}", mimetype="text/plain")

    yield test_file

    test_file.delete()


@fixture(scope="session")
def test_document(auth_test_clients):
    from pygsuite import Document

    test_doc = Document.get_safe(name=f"test-{uuid4()}")

    yield test_doc

    test_doc.delete()


@fixture(scope="session")
def test_form(auth_test_clients):
    from pygsuite import Form

    test_form = Form.get_safe(name=f"test-{uuid4()}")

    yield test_form

    test_form.delete()


@fixture(scope="session")
def test_presentation(auth_test_clients):
    from pygsuite import Presentation

    test_slides = Presentation.get_safe(name=f"test-{uuid4()}")

    yield test_slides

    test_slides.delete()


@fixture(scope="session")
def test_sheet(auth_test_clients):
    from pygsuite import Spreadsheet

    test_sheet = Spreadsheet.create(name=f"test-{uuid4()}")
    assert len(test_sheet.worksheets) == 1

    yield test_sheet

    test_sheet.delete()


@fixture(scope="session")
def test_image(auth_test_clients):
    raw = base64.b64decode(environ["TEST_IMAGE"].encode("utf-8"))
    uploader = ImageUploader(
        bucket=environ["TEST_BUCKET"], account_info=environ["TEST_GCS_ACCOUNT"]
    )
    url = uploader.signed_url_from_string(raw, "png")
    yield url
