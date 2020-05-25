from dataclasses import dataclass
from typing import Dict
from enum import Enum


from .base_element import BaseElement

class LineType(Enum):
    STRAIGHT:str
    BENT:str
    CURVED:str
    LINE_CATEGORY_UNSPECIFIED:str

@dataclass
class LineProperties:
    line_fill:str
    weight:str
    dash_style: str
    start_arrow:str
    end_arrow:str
    link:str
    start_connection:str
    end_connection:str

    @classmethod
    def from_api(cls, info):
        return LineProperties(info.get('lineFill'), info.get('weight'),
                              info.get('dashStyle'), info.get('startArrow'),
                              info.get('endArrow'), info.get('link'),
                              info.get('startConnection'),
                              info.get('endConnection'))


class Line(BaseElement):
    @classmethod
    def from_id(cls, id, presentation):
        return cls(element={"line": {}, "objectId": id}, presentation=presentation)

    def __init__(self, element, presentation):
        BaseElement.__init__(self, element, presentation)
        self._details = self._element.get("line")

    @property
    def id(self):
        return self._element["objectId"]

    def __repr__(self):
        return f'<Line type:{self.type}>'

    @property
    def type(self):
        return self._details.get("lineType")

    @property
    def category(self):
        return self._details.get("lineCategory")

    @property
    def properties(self):
        return LineProperties(self._details.get("lineProperties"))
