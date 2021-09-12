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


class FileTypes(Enum):
    SHEETS = "application/vnd.google-apps.spreadsheet"
    DOCS = "application/vnd.google-apps.document"
    SLIDES = "application/vnd.google-apps.presentation"
    FOLDER = "application/vnd.google-apps.folder"
    PDF = "application/pdf"
    UNKNOWN = ""

    def __str__(self):
        return self.value
