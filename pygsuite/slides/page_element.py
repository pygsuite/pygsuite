from .page_elements.base_element import BaseElement
from .page_elements.image import Image
from .page_elements.shape import Shape
from .page_elements.table import Table
from .page_elements.line import Line


class PageElement(object):
    def __init__(self, element, presentation):
        self._element = element
        self._presentation = presentation

    def __new__(cls, element, presentation):
        if element.get("shape"):
            return Shape(element, presentation)
        elif element.get("table"):
            return Table(element, presentation)
        elif element.get("image"):
            return Image(element, presentation)
        elif element.get("line"):
            return Line(element, presentation)
        else:
            return BaseElement(element, presentation)
