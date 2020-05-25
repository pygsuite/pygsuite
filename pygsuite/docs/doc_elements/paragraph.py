from pygsuite.docs.doc_elements import BaseElement
from pygsuite.common.style import TextStyle, ParagraphStyle

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

    def __repr__(self):
        return f"<Paragraph: {self.text[0:10]}.../>"

    @property
    def elements(self):
        return [ParagraphElement(elem, self._document) for elem in self._paragraph.get("elements")]

    @property
    def text(self):
        return "".join([element.text for element in self.elements if isinstance(element, TextRun)])

    @text.setter
    def text(self, text: str):
        self.delete()
        # TODO: combine with parent?
        self._document._mutation(
            [
                # {
                #     "deleteContentRange": {
                #         "range": {
                #             "segmentId": None,
                #             "startIndex": self.start_index,
                #             "endIndex": self.end_index - 1 if self._last else self.end_index,
                #         }
                #     }
                # },
                {
                    "insertText": {
                        "text": text,
                        "location": {"segmentId": None, "index": self.start_index},
                    }
                }
            ]
        )

    @property
    def style(self):
        return TextStyle.from_doc_style(self._paragraph.get("paragraphStyle"))

    @style.setter
    def style(self, style: ParagraphStyle = None):
        fields, style = style.to_doc_style("paragraph")
        self._document._mutation(
            [
                {
                    "updateParagraphStyle": {
                        "range": {
                            "startIndex": self.start_index,
                            "endIndex": self.end_index - 1 if self._last else self.end_index,
                        },
                        "paragraphStyle": style,
                        "fields": fields,
                    }
                }
            ]
        )

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
