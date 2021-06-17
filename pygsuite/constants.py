from os import environ, path


# AUTH
def get_credentials():
    dirname = path.dirname(path.dirname(__file__))
    return path.join(dirname, "credentials.json")


CREDENTIALS = environ.get("GOOGLE_APPLICATION_CREDENTIALS") or get_credentials()

# COMMON

# SHEETS
SHEETS_MAX_COLUMN_NUMBER = 18278

# DOCS

# SLIDES
