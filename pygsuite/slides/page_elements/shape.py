from dataclasses import dataclass
from typing import Dict

from .base_element import BaseElement


@dataclass
class Text:
    base: Dict

    @property
    def text(self):
        base = ""
        for el in self.base.get("textElements") or []:
            if el.get("textRun"):
                base += el.get("textRun")["content"]
        return base


class Shape(BaseElement):
    @classmethod
    def from_id(cls, id, presentation):
        return cls(element={"shape": {}, "objectId": id}, presentation=presentation)

    def __init__(self, element, presentation):
        BaseElement.__init__(self, element, presentation)
        self._details = self._element.get("shape")

    @property
    def id(self):
        return self._element["objectId"]

    @property
    def text(self):
        text = self._element.get("text")
        if text:
            return Text(text).text
        else:
            return None

    @text.setter
    def text(self, text: str):
        self.delete_text()
        self.add_text(text)

    def delete_text(self):
        if self.text:
            reqs = [{"deleteText": {"objectId": self.id, "textRange": {"type": "ALL"}}}]
            self._presentation._mutation(reqs=reqs)

    def add_text(self, text):
        reqs = [{"insertText": {"objectId": self.id, "insertionIndex": 0, "text": text}}]
        self._presentation._mutation(reqs=reqs)
