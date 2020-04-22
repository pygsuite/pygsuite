from .doc_elements.base_element import BaseElement
from .doc_elements.paragraph import Paragraph
from .doc_elements.section_break import SectionBreak
from .doc_elements.table import Table


# from .doc_elements.image import Image


class DocElement(object):
    def __init__(self, element, document, last: bool = False):
        self._element = element
        self._document = document

    def __new__(cls, element, document, last):
        if element.get("paragraph"):
            return Paragraph(element, document, last)
        elif element.get("table"):
            return Table(element, document, last)
        elif element.get("sectionBreak"):
            return SectionBreak(element, document, last)
        else:
            return BaseElement(element, document, last)
