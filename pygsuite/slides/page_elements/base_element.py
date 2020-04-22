from dataclasses import dataclass
from typing import Dict

from pygsuite.slides.page_elements.placeholder import Placeholder


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


class BaseElement(object):
    def __init__(self, element, presentation):
        self._element = element
        self._presentation = presentation
        self._details = {}

    @property
    def id(self):
        return self._element["objectId"]

    @property
    def position(self):
        return (self._element["transform"]["scaleX"], self._element["transform"]["scaleY"])

    def delete(self):
        reqs = [{"deleteObject": {"objectId": self.id}}]
        self._presentation._mutation(reqs)

    def update_text(self, text, bullets=False, **kwargs):
        reqs = [
            {"deleteText": {"objectId": self.id, "textRange": {"type": "ALL"}}},
            {"insertText": {"objectId": self.id, "text": text, "insertionIndex": 0}},
        ]

        if bullets and text:
            reqs.append(
                {"createParagraphBullets": {"objectId": self.id, "textRange": {"type": "ALL"}}}
            )

        return self._presentation._mutation(reqs)

    @property
    def children(self):
        return [self]

    @property
    def placeholder(self):
        check = self._details.get("placeholder")
        if check:
            return Placeholder(check)
