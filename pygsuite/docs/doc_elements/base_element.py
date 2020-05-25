"""{
  "startIndex": integer,
  "endIndex": integer,

  // Union field content can be only one of the following:
  "paragraph": {
    object (Paragraph)
  },
  "sectionBreak": {
    object (SectionBreak)
  },
  "table": {
    object (Table)
  },
  "tableOfContents": {
    object (TableOfContents)
  }
  // End of list of possible types for union field content.
}"""

from dataclasses import dataclass
from typing import Dict


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
    def __init__(self, element, document, last):
        self._element = element
        self._document = document
        self._last = last

    @property
    def id(self):
        return self._element["objectId"]

    # @property
    # def position(self):
    #     return (self._element['transform']['scaleX'], self._element['transform']['scaleY'])

    def delete(self):
        reqs = [{"deleteObject": {"objectId": self.id}}]
        self._document._mutation(reqs)

    def update_text(self, text, bullets=False, **kwargs):
        reqs = [
            {"deleteText": {"objectId": self.id, "textRange": {"type": "ALL"}}},
            {"insertText": {"objectId": self.id, "text": text, "insertionIndex": 0}},
        ]

        if bullets and text:
            reqs.append(
                {"createParagraphBullets": {"objectId": self.id, "textRange": {"type": "ALL"}}}
            )

        return self._document._mutation(reqs)

    @property
    def children(self):
        return [self]

    @property
    def end_index(self):
        return self._element.get("endIndex")

    @property
    def start_index(self):
        return self._element.get("startIndex")
