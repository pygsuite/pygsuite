from pygsuite.docs.doc_elements.paragraph_elements.base_paragraph_element import (
    BaseParagraphElement,
)


class AutoText(BaseParagraphElement):
    def __init__(self, element, presentation):
        BaseParagraphElement.__init__(self, element, presentation)
        self._detail = element.get("textRun")

    @property
    def content(self):
        return self._detail.get("content")

    def style(self):
        return self._detail.get("style")
