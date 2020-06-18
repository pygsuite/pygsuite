from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pygsuite.slides.page_elements.common import Text
from .base_element import BaseElement


class LineType(Enum):
    STRAIGHT: str
    BENT: str
    CURVED: str
    LINE_CATEGORY_UNSPECIFIED: str


class ArrowStyle(Enum):
    NONE = 0
    STEALTH_ARROW = 1
    FILL_ARROW = 2
    FILL_CIRCLE = 3
    FILL_SQUARE = 4
    FILL_DIAMOND = 5
    OPEN_ARROW = 6
    OPEN_CIRCLE = 7
    OPEN_SQUARE = 8
    OPEN_DIAMOND = 9

    def to_api_repr(self):
        return self.name


@dataclass
class LineConnection:
    object_id: str
    conn_index: int

    def to_api_repr(self):
        return {"connectedObjectId": self.object_id, "connectionSiteIndex": self.conn_index}


@dataclass
class LineProperties:
    line_fill: Optional[str] = None
    weight: Optional[int] = None
    dash_style: Optional[str] = None
    start_arrow: Optional[ArrowStyle] = None
    end_arrow: Optional[ArrowStyle] = None
    link: Optional[str] = None
    start_connection: Optional[LineConnection] = None
    end_connection: Optional[LineConnection] = None

    @classmethod
    def from_api(cls, info):
        return LineProperties(
            info.get("lineFill"),
            info.get("weight"),
            info.get("dashStyle"),
            info.get("startArrow"),
            info.get("endArrow"),
            info.get("link"),
            info.get("startConnection"),
            info.get("endConnection"),
        )

    def to_api_repr(self, line_id):
        fields = []
        properties = {}
        base = {
            "updateLineProperties": {
                "objectId": line_id,
                # "fields": "startConnection",
                # "lineProperties": {"startConnection": conn.to_api_repr()},
            }
        }
        if self.start_connection:
            key = "startConnection"
            fields.append(key)
            properties[key] = self.start_connection.to_api_repr()
        if self.end_connection:
            key = "endConnection"
            fields.append(key)
            properties[key] = self.end_connection.to_api_repr()
        if self.start_arrow:
            key = "startArrow"
            fields.append(key)
            properties[key] = self.start_arrow.to_api_repr()
        if self.start_arrow:
            key = "endArrow"
            fields.append(key)
            properties[key] = self.end_arrow.to_api_repr()
        base["updateLineProperties"]["fields"] = ",".join(fields)
        base["updateLineProperties"]["lineProperties"] = properties
        return base


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
        return f"<Line type:{self.type}>"

    @property
    def type(self):
        return self._details.get("lineType")

    @property
    def category(self):
        return self._details.get("lineCategory")

    @property
    def properties(self):
        return LineProperties(self._details.get("lineProperties"))

    @property
    def start_connection(self):
        base = self._details.get("lineProperties").get("startConnection")
        if not base:
            return None
        else:
            return LineConnection(base.get("connectedObjectId"), base.get("connectionSiteIndex"))

    @start_connection.setter
    def start_connection(self, conn: LineConnection):
        reqs = [
            {
                "updateLineProperties": {
                    "objectId": self.id,
                    "fields": "startConnection",
                    "lineProperties": {"startConnection": conn.to_api_repr()},
                }
            }
        ]
        self._presentation._mutation(reqs=reqs)

    @property
    def end_connection(self):
        base = self._details.get("lineProperties").get("endConnection")
        if not base:
            return None
        else:
            return LineConnection(base.get("connectedObjectId"), base.get("connectionSiteIndex"))

    @end_connection.setter
    def end_connection(self, conn: LineConnection):
        reqs = [
            {
                "updateLineProperties": {
                    "objectId": self.id,
                    "fields": "endConnection",
                    "lineProperties": {"endConnection": conn.to_api_repr()},
                }
            }
        ]
        self._presentation._mutation(reqs=reqs)

    @property
    def text(self):
        text = self._details.get("text")
        if text:
            return Text(text).text
        else:
            return None
