from json import loads, dumps
from os import environ, path
from uuid import uuid4

from pytest import fixture

from pygsuite import Clients

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
def test_document(auth_test_clients):
    from pygsuite import Document

    yield Document.get_safe(title=f"test-{uuid4()}")

    # yield Document.get_safe(title=f"test-static")


@fixture(scope="session")
def test_presentation(auth_test_clients):
    from pygsuite import Presentation

    yield Presentation.get_safe(title=f"test-{uuid4()}")

    # yield Document.get_safe(title=f"test-static")
