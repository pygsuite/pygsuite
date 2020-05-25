from json import loads
from os import environ
from pytest import fixture
from pygsuite import Clients


@fixture(scope="session")
def auth_test_clients():
    from google.oauth2.credentials import Credentials

    token = loads(environ["TEST_AUTH"])
    assert isinstance(token, dict)
    creds = Credentials(**token)
    Clients.authorize(creds)
