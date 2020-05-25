from json import loads
from os import environ
from pytest import fixture
from pygsuite import Clients
from uuid import uuid4


@fixture(scope="session")
def auth_test_clients():
    from google.oauth2.credentials import Credentials

    token = loads(environ["TEST_AUTH"])
    assert isinstance(token, dict)
    creds = Credentials(**token)
    Clients.authorize(creds)


@fixture(scope="session")
def test_document(auth_test_clients):
    from pygsuite import Document

    yield Document.get_safe(title=f"test-{uuid4()}")

    # yield Document.get_safe(title=f"test-static")


@fixture(scope="session")
def test_presentation(auth_test_clients):
    from pygsuite import Presentation

    yield Presentation.get_safe(title=f"test-{uuid4()}")

    # yield Document.get_safe(title=f"test-static")
