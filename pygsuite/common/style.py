from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Dict, Union


@dataclass
class Link:
    url: str
    bookmark_id: str
    heading_id: str


def hex_to_rgb(input: str):
    if input.startswith("#"):
        input = input[1:]
    return tuple(int(input[i : i + 2], 16) / 255.0 for i in (0, 2, 4))


def doc_color_to_color(info: Optional[dict]):
    if not info:
        return None
    base = info.get("color")
    if not base:
        return None
    base = base.get("rgbColor")
    if not base:
        return
    return Color(red=base["red"], green=base["green"], blue=base["blue"])


def doc_link_to_link(info: dict):
    if not info:
        return None
    # TODO: identify link format for these:
    # info.get('bookmarkId'), info.get('headingId')
    return info.get("url")  # Link(info.get('url'), info.get('bookmarkId'), info.get('headingId'))


@dataclass
class Color:
    hex: str = None
    red: float = None
    blue: float = None
    green: float = None
    alpha: float = None

    def __post_init__(self):

        assert self.hex or (
            self.red is not None and self.blue is not None and self.green is not None
        )
        if self.hex:
            self.red, self.green, self.blue = hex_to_rgb(self.hex)

    def to_json(self):

        return {"color": {"rgbColor": {"red": self.red, "green": self.green, "blue": self.blue}}}

    def to_sheet_style(self):

        base = {"red": self.red, "green": self.green, "blue": self.blue}

        if self.alpha is not None:
            base["alpha"] = self.alpha

        return base

    def to_slide_style(self):

        base = {"color": {"rgbColor": {"red": self.red, "green": self.green, "blue": self.blue}}}

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
    font_unit: Optional[str] = "PT"

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
            base["foregroundColor"] = self.color.to_sheet_style()
            masks.append("foregroundColor")
        if self.font is not None:
            base["fontFamily"] = self.font
            masks.append("fontFamily")

        return masks, base

    @classmethod
    def from_doc_style(cls, info):
        if info.get("namedStyleType"):
            return DefaultFonts[info.get("namedStyleType")]
        return TextStyle(
            font_size=info.get("fontSize").get("magnitude"),
            font_unit=info.get("fontSize").get("unit"),
            font=info.get("font"),
            font_weight=info.get("fonWeight"),
            color=doc_color_to_color(info.get("color")),
            background_color=doc_color_to_color(info.get("backgroundColor")),
            bold=info.get("bold"),
            italic=info.get("italic"),
            strikethrough=info.get("strikethrough"),
            small_caps=info.get("smallCaps"),
            underline=info.get("underline"),
            link=doc_link_to_link(info.get("link")),
        )


class BorderStyle(Enum):
    NONE = "NONE"
    DOTTED = "DOTTED"
    DASHED = "DASHED"
    SOLID = "SOLID"
    SOLID_MEDIUM = "SOLID_MEDIUM"
    SOLID_THICK = "SOLID_THICK"
    DOUBLE = "DOUBLE"


class BorderPosition(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    INNER_HORIZONTAL = "innerHorizontal"
    INNER_VERTICAL = "innerVertical"


@dataclass
class Border:
    """Dataclass to represent a Border object for a border along a cell.

    Google documentation: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/cells#Border
    """

    BORDER_STYLES = ["NONE", "DOTTED", "DASHED", "SOLID", "SOLID_MEDIUM", "SOLID_THICK", "DOUBLE"]
    COLOR_STYLES = ["rgbColor", "themeColor"]
    THEME_COLOR_TYPES = [
        "TEXT",
        "BACKGROUND",
        "ACCENT1",
        "ACCENT2",
        "ACCENT3",
        "ACCENT4",
        "ACCENT5",
        "ACCENT6",
        "LINK",
    ]

    position: str
    style: BorderStyle
    color: Color
    color_style: Optional[Union[str, Color]] = None

    def to_json(self):

        # assert self.style in self.BORDER_STYLES

        base = {"style": self.style.value, "color": self.color.to_sheet_style()}

        if self.color_style is not None:
            assert self.color_style in self.COLOR_STYLES
            if self.color_style == "rgbColor":
                assert isinstance(self.color_style, Color)
                base["colorStyle"] = self.color_style.to_sheet_style()
            elif self.color_style == "themeColor":
                assert self.color_style in self.THEME_COLOR_TYPES
                base["themeColor"] = self.color_style

        return base


class DefaultFonts(Enum):
    NORMAL_TEXT = TextStyle(font_size=11, font="arial", color=Color(hex="#000000"))
    TITLE = TextStyle(font_size=26, font="arial", color=Color(hex="#000000"))
    SUBTITLE = TextStyle(font_size=15, font="arial", color=Color(hex="#666666"))
    HEADING1 = TextStyle(font_size=20, font="arial", color=Color(hex="#000000"))
    HEADING2 = TextStyle(font_size=16, font="arial", color=Color(hex="#666666"))
    HEADING3 = TextStyle(font_size=14, font="arial", color=Color(hex="#434343"))
    HEADING4 = TextStyle(font_size=12, font="arial", color=Color(hex="#666666"))
    HEADING5 = TextStyle(font_size=11, font="arial", color=Color(hex="#666666"))
    HEADING6 = TextStyle(font_size=11, font="arial", italic=True, color=Color(hex="#666666"))

    def to_doc_style(self):
        return self.value.to_doc_style()


@dataclass
class ParagraphStyle:
    alignment: str
    line_space: int
    direction: str
    spacing_mode: str
    space_above: str
    space_below: str
    border_between: str
    border_top: BorderStyle
    keep_lines_together: bool
    keep_with_next: bool
    avoid_widow_and_orphan: bool
    shading: str

    def to_doc_style(self) -> Tuple[str, Dict]:  # noqa: C901
        base = {}
        masks = []
        if self.alignment is not None:
            base["alignment"] = {"alignment": self.alignment}
            masks.append("alignment")
        # TODO: validate all of these
        for attr in [
            "line_space",
            "direction",
            "spacing_mode",
            "space_above",
            "space_below",
            "border_between",
            "border_top",
            "keep_lines",
            "keep_with_next",
            "avoid_widow_and_orphan",
            "shading",
        ]:
            test = getattr(self, attr)
            if test:
                components = attr.split("_")
                name = components[0] + "".join([component.title() for component in components])
                base[name] = {name: test}
                masks.append(name)
        return ",".join(masks), base

    def to_sheet_style(self) -> Tuple[list, Dict]:  # noqa: C901
        raise NotImplementedError

    @classmethod
    def from_doc_style(cls, info):
        if info.get("namedStyleType"):
            return DefaultFonts[info.get("namedStyleType")]
        return ParagraphStyle(**info)
