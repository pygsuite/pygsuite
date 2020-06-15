from typing import Dict, Tuple
from uuid import uuid4


from pygsuite.slides.page_elements.placeholder import Placeholder
from .page_element import PageElement


class Layout(object):
    def __init__(self, layout, presentation):
        self._layout = layout
        self._presentation = presentation

    def __repr__(self):
        return f'Layout<name:"{self.display_name}">'

    @property
    def elements(self):
        return [
            PageElement(element, self._presentation) for element in self._layout.get("pageElements")
        ]

    @property
    def layout_properties(self):
        return self._layout["layoutProperties"]

    @property
    def display_name(self):
        return self.layout_properties["displayName"]

    @property
    def id(self):
        return self._layout["objectId"]

    def _get_smart_placeholder(self, test_str):

        matches = []
        for key in self.placeholders:
            if test_str in key:
                matches.append(key)
        if len(matches) > 1:
            raise ValueError(
                f"Placeholder key {test_str} was not specific enough - could match any of {matches}"
            )
        if len(matches) == 0:
            raise ValueError(f"No match found for placeholder key {test_str}")
        return self.placeholders[matches[0]]

    def build_reference_map(self, key, val) -> Tuple[Dict, Dict]:

        if "_" in key:
            details = self.placeholders[key]
        else:
            details = self._get_smart_placeholder(key)
        obj_id = str(uuid4()) + key
        return (
            {"insertText": {"objectId": obj_id, "text": val}},
            {
                "layoutPlaceholder": {
                    "type": details.type,
                    "index": details.index,
                    "parentObjectId": details.parent_id,
                },
                "objectId": obj_id,
            },
        )

    @property
    def placeholders(self) -> Dict[str, Placeholder]:
        base = [obj.placeholder for obj in self.elements if obj.placeholder]

        return {str(obj): obj for obj in base}
