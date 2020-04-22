from os import environ, path


def get_credentials():
    dirname = path.dirname(path.dirname(__file__))
    return path.join(dirname, "credentials.json")


CREDENTIALS = environ.get("GOOGLE_APPLICATION_CREDENTIALS") or get_credentials()
