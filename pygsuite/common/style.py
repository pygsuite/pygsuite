from dataclasses import dataclass
from typing import Optional


@dataclass
class Color:
    red: int
    blue: int
    green: int

    def to_json(self):
        return {"color": {"rgbColor": {"red": self.red, "green": self.green, "blue": self.blue}}}


@dataclass
class TextStyle:
    font_size: Optional[int]
    font: Optional[str]
    foreground_color: Optional[Color]
    bold: bool = False
    italic: bool = False
    small_caps: bool = False
    underline: bool = False
    link: str = None
