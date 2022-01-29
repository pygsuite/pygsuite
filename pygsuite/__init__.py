from pygsuite.auth.authorization import Clients
from pygsuite.common.style import DefaultFonts, TextStyle, Color
from pygsuite.docs import Document
from pygsuite.sheets import Spreadsheet
from pygsuite.slides import Presentation
from pygsuite.images import ImageUploader
from pygsuite.drive.drive import Drive
from pygsuite.drive.file import File
from pygsuite.drive.folder import Folder
from pygsuite.enums import UserType, PermissionType

__version__ = "0.0.17"
__author__ = "Ethan Dickinson <ethan.dickinson@gmail.com>"
__all__ = [
    "Clients",
    "Color",
    "DefaultFonts",
    "Document",
    "Drive",
    "File",
    "Folder",
    "PermissionType",
    "Presentation",
    "Spreadsheet",
    "TextStyle",
    "ImageUploader",
    "UserType",
]  # type: ignore
