from pygsuite.docs.doc_elements import BaseElement

from .paragraph_elements import (
    AutoText,
    ColumnBreak,
    HorizontalRule,
    PageBreak,
    TextRun,
    FootnoteReference,
    Equation,
)


# from .doc_elements.image import Image
class ParagraphElement(object):
    def __init__(self, element, document):

        self._element = element
        self._document = document

    def __new__(cls, element, document):
        if element.get("autoText"):
            return AutoText(element, document)
        elif element.get("textRun"):
            return TextRun(element, document)
        elif element.get("ColumnBreak"):
            return ColumnBreak(element, document)
        elif element.get("HorizontalRule"):
            return HorizontalRule(element, document)
        elif element.get("PageBreak"):
            return PageBreak(element, document)
        elif element.get("FootnoteReference"):
            return FootnoteReference(element, document)
        elif element.get("Equation"):
            return Equation(element, document)


class Paragraph(BaseElement):
    def __init__(self, element, document, last):
        BaseElement.__init__(self, element=element, document=document, last=last)
        self._paragraph = self._element.get("paragraph")

    @property
    def elements(self):
        return [ParagraphElement(elem, self._document) for elem in self._paragraph.get("elements")]

    @property
    def text(self):
        return "".join(
            [element.content for element in self.elements if isinstance(element, TextRun)]
        )

    #
    def delete(self):
        end_index = self.end_index - 1 if self._last else self.end_index
        if self.start_index == end_index:
            return
        self._document._mutation(
            [
                {
                    "deleteContentRange": {
                        "range": {
                            "segmentId": None,
                            "startIndex": self.start_index,
                            "endIndex": self.end_index - 1 if self._last else self.end_index,
                        }
                    }
                }
            ]
        )
