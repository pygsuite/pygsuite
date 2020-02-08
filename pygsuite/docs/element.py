from dataclasses import dataclass
from typing import List, Dict

from .doc_elements.paragraph import Paragraph
from .doc_elements.base_element import BaseElement
from .doc_elements.table import Table
# from .doc_elements.image import Image

class DocElement(object):
    def __init__(self, element, document):
        self._element = element
        self._document = document

    def __new__(cls, element, document):
        if element.get('paragraph'):
            return Paragraph(element, document)
        elif element.get('table'):
            return Table(element, document)
        # elif element.get('image'):
        #     return Image(element, document)
        else:
            return BaseElement(element, document)


