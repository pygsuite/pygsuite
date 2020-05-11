from dataclasses import dataclass
from typing import Optional


@dataclass
class Color:
    red: int
    blue: int
    green: int
    alpha: int = 1

    def to_json(self):
        return {
            "red": self.red,
            "green": self.green,
            "blue": self.blue,
            "alpha": self.alpha
        }


@dataclass
class TextStyle:
    font_size: Optional[int]
    font: Optional[str]
    foreground_color: Optional[Color]
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    small_caps: bool = False
    underline: bool = False
    link: str = None

    def to_json(self):
        json_obj = {
            "bold": self.bold,
            "italic": self.italic,
            "strikethrough": self.strikethrough,
            "underline": self.underline
        }

        if self.font_size:
            json_obj["fontSize"] = self.font_size

        if self.font:
            json_obj["fontFamily"] = self.font

        if self.foreground_color:
            json_obj["foregroundColor"] = self.foreground_color.to_json()

        return json_obj


@dataclass
class BorderStyle:
    """Dataclass to represent a Border object for a border along a cell.

    Google documentation: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#Border 
    """

    BORDER_STYLES = ["NONE", "DOTTED", "DASHED", "SOLID", "SOLID_MEDIUM", "SOLID_THICK", "DOUBLE"]

    position: str
    style: str
    # width: Optional[int] DEPRECATED by Google
    color: Color
    # TODO: if "themeColor" is given, we need to make color optional, etc.
    color_style: str = "rgbColor"

    def to_json(self):

        assert self.style in self.BORDER_STYLES

        return {
            "style": self.style,
            "color": self.color.to_json(),
            # "colorStyle": self.color_style
        }
