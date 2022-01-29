from os import environ, path

from pygsuite.enums import GoogleDocFormat


# AUTH
def get_credentials():
    dirname = path.dirname(path.dirname(__file__))
    return path.join(dirname, "credentials.json")


CREDENTIALS = environ.get("GOOGLE_APPLICATION_CREDENTIALS") or get_credentials()

# COMMON

# DRIVE
FILE_MIME_TYPE_MAP = {
    GoogleDocFormat.DOCS: {
        ".html": "text/html",
        ".txt": "text/plain",
        ".rtf": "application/rtf",
        ".odt": "application/vnd.oasis.opendocument.text",
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".doc": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".epub": "application/epub+zip",
    },
    GoogleDocFormat.SHEETS: {
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".ods": "application/x-vnd.oasis.opendocument.spreadsheet",
        ".pdf": "application/pdf",
        ".csv": "text/csv",
        ".tsv": "text/tab-separated-values",
    },
    GoogleDocFormat.DRAWINGS: {
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".png": "image/png",
        ".svg": "image/svg+xml",
        ".pdf": "application/pdf",
    },
    GoogleDocFormat.SLIDES: {
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".ppt": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".odp": "application/vnd.oasis.opendocument.presentation",
        ".pdf": "application/pdf",
        ".txt": "text/plain",
    },
    GoogleDocFormat.SCRIPTS: {
        ".json": "application/vnd.google-apps.script+json",
    },
}

# Each chunk of a Drive File upload cannot exceed 50MB
DRIVE_FILE_MAX_SINGLE_UPLOAD_SIZE = 50000000

# SHEETS
SHEETS_MAX_COLUMN_NUMBER = 18278

# DOCS

# SLIDES
