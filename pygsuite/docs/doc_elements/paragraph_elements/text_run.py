from pygsuite.docs.doc_elements.paragraph_elements.base_paragraph_element import (
    BaseParagraphElement,
)
from pygsuite.common.style import TextStyle


class TextRun(BaseParagraphElement):
    def __init__(self, element, presentation):
        BaseParagraphElement.__init__(self, element, presentation)
        self._detail = element.get("textRun")

    def __repr__(self):
        return f"<TextRun: {self.text[0:10]}/>"

    @property
    def text(self):
        return self._detail.get("content")

    @text.setter
    def text(self, text: str):
        self.delete()
        # TODO: combine with parent?
        self._document._mutation(
            [
                # {
                #     "deleteContentRange": {
                #         "range": {
                #             "segmentId": None,
                #             "startIndex": self.start_index,
                #             "endIndex": self.end_index - 1 if self._last else self.end_index,
                #         }
                #     }
                # },
                {
                    "insertText": {
                        "text": text,
                        "location": {"segmentId": None, "index": self.start_index},
                    }
                }
            ]
        )

    @property
    def style(self):
        return TextStyle.from_doc_style(self._detail.get("textStyle"))

    @style.setter
    def style(self, style: TextStyle = None):
        fields, style = style.to_doc_style()
        self._document._mutation(
            [
                {
                    "updateTextStyle": {
                        "range": {"startIndex": self.start_index, "endIndex": self.end_index},
                        "textStyle": style,
                        "fields": fields,
                    }
                }
            ]
        )

    def delete(self):
        end_index = self.end_index
        if self.start_index == end_index:
            return
        self._document._mutation(
            [
                {
                    "deleteContentRange": {
                        "range": {
                            "segmentId": None,
                            "startIndex": self.start_index,
                            "endIndex": self.end_index,
                        }
                    }
                }
            ]
        )
