from typing import List

from pygsuite.common.style import TextStyle
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
    def content(self) -> List[DocElement]:
        content_len = len(self._body.get("content"))
        return [
            DocElement(element, self._document, idx == content_len - 1)
            for idx, element in enumerate(self._body.get("content"))
        ]

    def delete(self, flush=True):
        # save the last character of the last element
        for object in reversed(self.content):
            object.delete()
        if flush:
            self._document.flush()
        self.content = []

    @content.setter
    def content(self, x):
        self._body["content"] = x

    @property
    def start_index(self):
        return self.content[0].start_index

    @property
    def end_index(self):
        return self.content[-1].end_index

    #
    def __getitem__(self, item):
        return self.content[item]

    def __setitem__(self, index, value, style=None):
        self.content[index] = value

    def add_text(self, text: str, position: int = None, style: TextStyle = None):
        if style and not position:
            # if there are pending changes
            # we need to flush them to infer proper style positioning
            self._document.flush()
        message = {"insertText": {"text": text}}
        if position is not None:
            message["insertText"]["location"] = {"index": position}
        else:
            message["insertText"]["endOfSegmentLocation"] = {}
        queued = [message]

        if style:
            start = position

            if position is None:
                start = self.content[-1].end_index - 1 if self.content else 1

            end = start + len(text)

            fields, style = style.to_doc_style()
            queued.append(
                {
                    "updateTextStyle": {
                        "range": {"startIndex": start, "endIndex": end},
                        "textStyle": style,
                        "fields": fields,
                    }
                }
            )

        self._document._mutation(queued)

        if style and not position:
            # we need to force a flush here, as the assumed indices
            # will not be accurate after multiple queued changes
            self._document.flush()

    def add_image(self, uri, position=None):
        message = {
            "insertInlineImage": {
                "uri": uri,
                # "objectSize": {
                #     object (Size)
                # }
            }
        }
        if position:
            message["insertInlineImage"]["location"] = {"index": position}
        else:
            message["insertInlineImage"]["endOfSegmentLocation"] = {}
        self._document._mutation([message])

    def style(self, style: TextStyle, start: int, end: int):
        # TODO: finish this method
        fields, style = style.to_doc_style()
        message = {
            "updateTextStyle": {
                "textStyle": style,
                "range": {"startIndex": start, "endIndex": end},
                "fields": fields,
            }
        }
        return message
