from os import environ, path


# AUTH
def get_credentials():
    dirname = path.dirname(path.dirname(__file__))
    return path.join(dirname, "credentials.json")


CREDENTIALS = environ.get("GOOGLE_APPLICATION_CREDENTIALS") or get_credentials()

# COMMON

# DRIVE

# Each chunk of a Drive File upload cannot exceed 50MB
DRIVE_FILE_MAX_SINGLE_UPLOAD_SIZE = 50000000

# SHEETS
SHEETS_MAX_COLUMN_NUMBER = 18278

# DOCS

# SLIDES
