from dataclasses import dataclass

from pygsuite.common.style import Color
from pygsuite.slides.page_elements.common import Text
from .base_element import BaseElement


@dataclass
class BackgroundFill:
    state: str
    solid_fill: Color


@dataclass
class ShapeProperties:
    shape_background_fill: Color = None
    outline: str = None
    shadow: str = None
    link: str = None
    content_alignment: str = None

    # def __post_init__(self):
    #     if isinstance(self.shape_background_fill):

    @classmethod
    def from_api_repr(cls, info: dict):
        if not info:
            return ShapeProperties()
        return ShapeProperties(
            info.get("shapeBackgroundFill"),
            info.get("outline"),
            info.get("shadow"),
            info.get("link"),
            info.get("contentAlignment"),
        )

    def to_api_repr(self):
        base = {}
        masks = []

        if self.shape_background_fill is not None:
            base["shapeBackgroundFill"] = {
                "propertyState": "RENDERED",
                "solidFill": self.shape_background_fill.to_slide_style(),
            }
            masks.append("shapeBackgroundFill")
        else:
            base["shapeBackgroundFill"] = {"propertyState": "NOT_RENDERED"}
            masks.append("shapeBackgroundFill")

        if self.outline is not None:
            base["outline"] = self.outline
            masks.append("outline")
        if self.shadow is not None:
            base["shadow"] = self.shadow
            masks.append("shadow")
        if self.link is not None:
            base["link"] = self.link
            masks.append("link")
        masks = ",".join(masks)
        return masks, base


class Shape(BaseElement):
    @classmethod
    def from_id(cls, id, presentation):
        return cls(element={"shape": {}, "objectId": id}, presentation=presentation)

    def __init__(self, element, presentation):
        BaseElement.__init__(self, element, presentation)
        self._details = self._element.get("shape")

    @property
    def id(self):
        return self._element["objectId"]

    def __repr__(self):
        return f"<Shape type:{self.type}>"

    @property
    def type(self):
        return self._details.get("shapeType")

    @property
    def text(self):
        text = self._details.get("text")
        if text:
            return Text(text).text
        else:
            return None

    @text.setter
    def text(self, text: str):
        self.delete_text()
        self.add_text(text)

    def delete_text(self):
        if self.text:
            reqs = [{"deleteText": {"objectId": self.id, "textRange": {"type": "ALL"}}}]
            self._presentation._mutation(reqs=reqs)

    def add_text(self, text):
        reqs = [{"insertText": {"objectId": self.id, "insertionIndex": 0, "text": text}}]
        self._presentation._mutation(reqs=reqs)

    @property
    def properties(self):
        return ShapeProperties.from_api_repr(self._details.get("shapeProperties"))

    @properties.setter
    def properties(self, value: ShapeProperties):
        masks, props = value.to_api_repr()
        reqs = [
            {
                "updateShapeProperties": {
                    "objectId": self.id,
                    "fields": masks,
                    "shapeProperties": props,
                }
            }
        ]
        self._presentation._mutation(reqs=reqs)

    @property
    def background_color(self):
        return self.properties.shape_background_fill

    @background_color.setter
    def background_color(self, color: Color):
        new = self.properties
        new.shape_background_fill = color
        self.properties = new

    @property
    def text_style(self):
        return

    @text_style.setter
    def text_style(self, val):
        pass
