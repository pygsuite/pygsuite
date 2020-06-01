from dataclasses import dataclass
from typing import List, Union

from jinja2 import Template, Environment, meta

from .page_element import PageElement, Table, Shape, Image, Line
from pygsuite.slides.element_properties import ElementProperties
from pygsuite.slides.enums import ShapeType
from pygsuite.utility.guids import get_guid


@dataclass
class FancyFont:
    lines: List
    font_size: float
    bullets: bool


class Slide(object):
    @classmethod
    def from_id(cls, id, presentation):
        slides = presentation.slides
        return [slide for slide in slides if slide.id == id][0]

    def __init__(self, slide, presentation):
        # TODO
        self._slide = slide
        self._properties = slide["slideProperties"]
        self._presentation = presentation

    @property
    def elements(self):
        elements = self._slide.get("pageElements")
        if not elements:
            return []
        return [PageElement(element, self._presentation) for element in elements]

    @property
    def id(self):
        return self._slide["objectId"]

    @property
    def tables(self):
        return [el for el in self.elements if isinstance(el, Table)]

    @property
    def shapes(self):
        return [el for el in self.elements if isinstance(el, Shape)]

    @property
    def images(self):
        return [el for el in self.elements if isinstance(el, Image)]

    def duplicate(self, append=True):
        # create a slide at the end of the presentation
        reqs = [{"duplicateObject": {"objectId": self.id}}]
        output = self._presentation._mutation(reqs=reqs, flush=True)[-1]["duplicateObject"][
            "objectId"
        ]

        if append:
            reqs = [
                {
                    "updateSlidesPosition": {
                        "slideObjectIds": [output],
                        "insertionIndex": len(self._presentation.slides),
                    }
                }
            ]
            self._presentation._mutation(reqs=reqs, flush=True)
        return output

    def template_text(self, dict):
        reqs = []
        for element in self.elements:
            for object in element.children:
                if object.text and any([key in object.text for key in dict]):
                    text = object.text
                    text = text.replace("’", "'")
                    text = text.replace("‘", "'")
                    env = Environment()
                    ast = env.parse(text)
                    vars = meta.find_undeclared_variables(ast)
                    if vars:
                        bullets = False
                        font_size = 8
                        render_dict = {key: dict[key] for key in dict if key in vars}
                        for var in render_dict:
                            # turn it into paragraphs if list
                            # and add bullets
                            if isinstance(render_dict[var], FancyFont):
                                ff_item = render_dict[var]
                                bullets = ff_item.bullets
                                font_size = ff_item.font_size
                                render_dict[var] = "\n".join(ff_item.lines)
                        new_text = Template(text).render(**render_dict)
                        if new_text != object.text:
                            reqs.append(
                                object.update_text(new_text, bullets=bullets, font_size=font_size)
                            )

        self._presentation._mutation(reqs=reqs)

    def add_image(self, url: str, properties: ElementProperties, id=None):
        id = id or get_guid()
        reqs = []

        reqs.append(
            {
                "createImage": {
                    "objectId": id,
                    "elementProperties": properties.to_slides_json(self.id),
                    "url": url,
                }
            }
        )
        self._presentation._mutation(reqs=reqs)
        return Image.from_id(id=id, presentation=self._presentation)

    #
    # def add_text(self, text):
    #     raise NotImplementedError

    def add_line(self, category, properties: ElementProperties, id=None):
        id = id or get_guid()
        reqs = []

        reqs.append(
            {
                "createLine": {
                    "objectId": id,
                    "elementProperties": properties.to_slides_json(self.id),
                    "category": category,
                }
            }
        )
        self._presentation._mutation(reqs=reqs)
        return Line.from_id(id=id, presentation=self._presentation)

    def add_word_art(self, text):
        raise NotImplementedError

    def add_table(self, table):
        raise NotImplementedError

    def add_shape(self, shape: Union[str, ShapeType], properties: ElementProperties, id=None):
        id = id or get_guid()
        reqs = []
        if isinstance(shape, ShapeType):
            shape = shape.name
        reqs.append(
            {
                "createShape": {
                    "objectId": id,
                    "elementProperties": properties.to_slides_json(self.id),
                    "shapeType": shape,
                }
            }
        )
        self._presentation._mutation(reqs=reqs)
        return Shape.from_id(id=id, presentation=self._presentation)
