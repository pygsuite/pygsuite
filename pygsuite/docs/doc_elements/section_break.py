from .paragraph_elements import (
    AutoText,
    ColumnBreak,
    HorizontalRule,
    PageBreak,
    TextRun,
    FootnoteReference,
    Equation,
)


class SectionBreak(object):
    def __init__(self, element, document, last):
        self._element = element
        self._document = document
        self._paragraph = self._element.get("paragraph")
        self._last = last

    @property
    def end_index(self):
        return self._element.get("endIndex")

    @property
    def start_index(self):
        return self._element.get("startIndex")

    @property
    def section_style(self):
        return self._element.get("sectionStyle")

    def delete(self):
        if not self.start_index:
            return
        if self.start_index == self.end_index:
            return
        self._document._mutation(
            [
                {
                    "deleteContentRange": {
                        "range": {
                            "segmentId": None,
                            "startIndex": self.start_index,
                            "endIndex": self.end_index,
                        }
                    }
                }
            ]
        )
