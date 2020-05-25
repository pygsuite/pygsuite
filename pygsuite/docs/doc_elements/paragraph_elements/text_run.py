from pygsuite.docs.doc_elements.paragraph_elements.base_paragraph_element import (
    BaseParagraphElement,
)


class TextRun(BaseParagraphElement):
    def __init__(self, element, presentation):
        BaseParagraphElement.__init__(self, element, presentation)
        self._detail = element.get("textRun")

    def __repr__(self):
        return f"<TextRun: {self.content[0:10]}/>"

    @property
    def content(self):
        return self._detail.get("content")

    @property
    def style(self):
        return self._detail.get("textStyle")
