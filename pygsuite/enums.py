from enum import Enum


class PermissionType(Enum):
    OWNER = "owner"
    ORGANIZER = "organizer"
    FILE_ORGANIZER = "fileOrganizer"
    WRITER = "writer"
    COMMENTER = "commenter"
    READER = "reader"


class UserType(Enum):
    USER = "user"
    GROUP = "group"
    DOMAIN = "domain"
    ANYONE = "anyone"


class MimeType(Enum):
    UNKNOWN = ""
    # Google MIME Types
    SHEETS = "application/vnd.google-apps.spreadsheet"
    DOCS = "application/vnd.google-apps.document"
    SLIDES = "application/vnd.google-apps.presentation"
    FOLDER = "application/vnd.google-apps.folder"
    # Some other common MIME Types for convenience:
    # Text files
    PLAIN_TEXT = "text/plain"
    HTML = "text/html"
    PDF = "application/pdf"
    # Microsoft Office files
    MS_WORD = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    MS_EXCEL = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    MS_POWERPOINT = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    # Image files
    JPEG = "image/jpeg"
    PNG = "image/png"
    SVG = "image/svg+xml"

    def __str__(self):
        return self.value


class GoogleDocFormat(Enum):
    DOCS = "Documents"
    SHEETS = "Spreadsheets"
    DRAWINGS = "Drawings"
    SLIDES = "Presentations"
    SCRIPTS = "App Scripts"
