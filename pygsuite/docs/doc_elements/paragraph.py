from .paragraph_elements import AutoText, ColumnBreak, HorizontalRule, PageBreak, TextRun, FootnoteReference, Equation


# from .doc_elements.image import Image
class ParagraphElement(object):
    def __init__(self, element, document):
        self._element = element
        self._document = document

    def __new__(cls, element, document):
        if element.get('autoText'):
            return AutoText(element, document)
        elif element.get('textRun'):
            return TextRun(element, document)
        elif element.get('ColumnBreak'):
            return ColumnBreak(element, document)
        elif element.get('HorizontalRule'):
            return HorizontalRule(element, document)
        elif element.get('PageBreak'):
            return PageBreak(element, document)
        elif element.get('FootnoteReference'):
            return FootnoteReference(element, document)
        elif element.get('Equation'):
            return Equation(element, document)


class Paragraph(object):
    def __init__(self, element, document, last):
        self._element = element
        self._document = document
        self._paragraph = self._element.get('paragraph')
        self.last = last

    @property
    def end_index(self):
        return self._element.get('endIndex')

    @property
    def start_index(self):
        return self._element.get('startIndex')

    @property
    def elements(self):
        return [ParagraphElement(elem, self._document) for elem in self._paragraph.get('elements')]

    @property
    def text(self):
        return ''.join([element.content for element in self.elements if isinstance(element, TextRun)])
#
    def delete(self):
        end_index = self.end_index-1 if self.last else self.end_index
        if self.start_index == end_index:
            return
        self._document._mutation([{'deleteContentRange': {'range': {
            "segmentId": None,
            "startIndex": self.start_index,
            "endIndex": self.end_index-1 if self.last else self.end_index
        }}}])

