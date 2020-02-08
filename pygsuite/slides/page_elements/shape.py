from .base_element import BaseElement
from dataclasses import dataclass
from typing import Dict



@dataclass
class Text():
    base:Dict

    @property
    def text(self):
        base = ''
        for el in self.base.get('textElements') or []:
            if el.get('textRun'):
                base += el.get('textRun')['content']
        return base

class Shape(BaseElement):
    def __init__(self, element, presentation):
        BaseElement.__init__(self,element, presentation)
        self._details = self._element.get('shape')

    @property
    def id(self):
        return self._element['objectId']

    @property
    def text(self):
        text = self._details.get('text')
        if text:
            return Text(text).text
        else:
            return None

