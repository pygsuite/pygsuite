from dataclasses import dataclass
from typing import Optional, Tuple, Dict


def hex_to_rgb(input: str):
    if input.startswith("#"):
        input = input[1:]
    return tuple(int(input[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


@dataclass
class Color:
    hex: str = None
    red: float = None
    blue: float = None
    green: float = None
    alpha: float = None

    def __post_init__(self):

        assert self.hex or (self.red and self.blue and self.green)
        if self.hex:
            self.red, self.green, self.blue = hex_to_rgb(self.hex)

    def to_json(self):

        return {
            "color": {
                "rgbColor": {
                    "red": self.red,
                    "green": self.green,
                    "blue": self.blue
                }
            }
        }

    def to_sheet_style(self):

        base = {
            "red": self.red,
            "green": self.green,
            "blue": self.blue,
        }

        if self.alpha is not None:
            base["alpha"] = self.alpha

        return base


@dataclass
class TextStyle:
    font_size: Optional[int] = None
    font: Optional[str] = None
    font_weight: Optional[int] = None
    color: Optional[Color] = None
    background_color: Optional[Color] = None
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    strikethrough: Optional[bool] = None
    small_caps: Optional[bool] = None
    underline: Optional[bool] = None
    link: str = None

    def to_doc_style(self) -> Tuple[str, Dict]:  # noqa: C901
        base = {}
        masks = []
        if self.font_size is not None:
            base["fontSize"] = {"magnitude": self.font_size, "unit": "PT"}
            masks.append("fontSize")
        if self.bold is not None:
            base["bold"] = self.bold
            masks.append("bold")
        if self.italic is not None:
            base["italic"] = self.italic
            masks.append("italic")
        if self.underline is not None:
            base["underline"] = self.underline
            masks.append("underline")
        if self.small_caps is not None:
            base["smallCaps"] = self.small_caps
            masks.append("smallCaps")
        if self.background_color is not None:
            base["backgroundColor"] = self.background_color.to_json()
            masks.append("backgroundColor")
        if self.color is not None:
            base["foregroundColor"] = self.color.to_json()
            masks.append("foregroundColor")
        if self.font is not None:
            if not base.get("weightedFontFamily"):
                base["weightedFontFamily"] = {}
            base["weightedFontFamily"]["fontFamily"] = self.font
            masks.append("weightedFontFamily.fontFamily")
        if self.font_weight is not None:
            if not base.get("weightedFontFamily"):
                base["weightedFontFamily"] = {}
                base["weightedFontFamily"]["fontFamily"] = "Arial"
            base["weightedFontFamily"]["weight"] = self.font_weight
            masks.append("weightedFontFamily.fontFamily")
            masks.append("weightedFontFamily.weight")

        return ",".join(masks), base

    def to_sheet_style(self) -> Tuple[list, Dict]:  # noqa: C901

        base = {}
        masks = []

        if self.font_size is not None:
            base["fontSize"] = {"magnitude": self.font_size, "unit": "PT"}
            masks.append("fontSize")
        if self.bold is not None:
            base["bold"] = self.bold
            masks.append("bold")
        if self.italic is not None:
            base["italic"] = self.italic
            masks.append("italic")
        if self.underline is not None:
            base["underline"] = self.underline
            masks.append("underline")
        if self.color is not None:
            base["foregroundColor"] = self.color.to_json()
            masks.append("foregroundColor")
        if self.font is not None:
            base["fontFamily"] = self.font
            masks.append("fontFamily")

        return masks, base


@dataclass
class BorderStyle:
    """Dataclass to represent a Border object for a border along a cell.

    Google documentation: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#Border 
    """

    BORDER_STYLES = ["NONE", "DOTTED", "DASHED", "SOLID", "SOLID_MEDIUM", "SOLID_THICK", "DOUBLE"]
    COLOR_STYLES = ["rgbColor", "themeColor"]

    position: str
    style: str
    color: Color
    # TODO: if "themeColor" is given, we need to make color optional, etc.
    color_style: str = "rgbColor"

    def to_json(self):

        assert self.style in self.BORDER_STYLES
        assert self.color_style in self.COLOR_STYLES

        return {
            "style": self.style,
            "color": self.color.to_json(),
            # "colorStyle": self.color_style
        }


class DefaultFonts:
    normal = TextStyle(font_size=11, font="arial", color=Color(hex="#000000"))
    title = TextStyle(font_size=26, font="arial", color=Color(hex="#000000"))
    subtitle = TextStyle(font_size=15, font="arial", color=Color(hex="#666666"))
    heading1 = TextStyle(font_size=20, font="arial", color=Color(hex="#000000"))
    heading2 = TextStyle(font_size=16, font="arial", color=Color(hex="#666666"))
    heading3 = TextStyle(font_size=14, font="arial", color=Color(hex="#434343"))
    heading4 = TextStyle(font_size=12, font="arial", color=Color(hex="#666666"))
    heading5 = TextStyle(font_size=11, font="arial", color=Color(hex="#666666"))
    heading6 = TextStyle(font_size=11, font="arial", italic=True, color=Color(hex="#666666"))
