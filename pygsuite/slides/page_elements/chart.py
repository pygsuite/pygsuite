from dataclasses import dataclass
from typing import Dict
from enum import Enum

from .base_element import BaseElement


class Chart(BaseElement):
    @classmethod
    def from_id(cls, id, presentation):
        return cls(element={"sheetsChart": {}, "objectId": id}, presentation=presentation)

    def __init__(self, element, presentation):
        BaseElement.__init__(self, element, presentation)
        self._details = self._element.get("sheetsChart")

    @property
    def id(self):
        return self._element["objectId"]

    def __repr__(self):
        return f"<Chart >"

    @property
    def spreadsheet_id(self):
        return self._details.get("spreadsheetId")

    @property
    def chart_id(self):
        return self._details.get("chartId")

    @property
    def content_url(self):
        return self._details.get("content_url")
