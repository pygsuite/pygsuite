from dataclasses import dataclass
from typing import List

from jinja2 import Template, Environment, meta
from pygsuite.docs.element import DocElement

class Body(object):
    #
    # @classmethod
    # def from_id(cls, id, document):
    #     slides = presentation.slides
    #     return [slide for slide in slides if slide.id == id][0]

    def __init__(self, body, document):
        # TODO
        self._body = body
        # self._properties = slide['slideProperties']
        self._document = document

    @property
    def content(self):
        return [DocElement(element, self._document) for element in self._body.get('content')]

    def __getitem__(self, item):
        return self.content[item]

    def __setitem__(self, index, value):
        self.content[index] = value