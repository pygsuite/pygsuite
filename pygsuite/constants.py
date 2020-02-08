from os import environ, path
from pygsuite.auth import Clients

def get_credentials():
    dirname = path.dirname(path.dirname(__file__))
    return path.join(dirname, 'credentials.json')

CREDENTIALS = environ.get('GOOGLE_APPLICATION_CREDENTIALS') or get_credentials()

CLIENTS = Clients(CREDENTIALS)
