from pygsuite.auth.authorization import Clients
from pygsuite.common.style import DefaultFonts, TextStyle, Color
from pygsuite.docs import Document
from pygsuite.sheets import Spreadsheet
from pygsuite.slides import Presentation
from pygsuite.images import ImageUploader
from pygsuite.drive import Drive

__version__ = "0.0.2"
__author__ = "Ethan Dickinson <ethan.dickinson@gmail.com>"
__all__ = [
    Clients,
    DefaultFonts,
    Spreadsheet,
    Document,
    Presentation,
    TextStyle,
    Color,
    ImageUploader,
    Drive,
]  # type: ignore
