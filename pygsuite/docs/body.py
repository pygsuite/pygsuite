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
        content_len = len(self._body.get('content'))
        return [DocElement(element, self._document, idx == content_len - 1) for idx, element in
                enumerate(self._body.get('content'))]

    def delete(self, flush=True):
        # save the last character of the last element
        for object in reversed(self.content):
            object.delete()
        if flush:
            self._document.flush()

    @content.setter
    def content(self, x):
        raise NotImplementedError

    @content.setter
    def content(self, x):
        raise NotImplementedError

    @property
    def start_index(self):
        return self.content[0].start_index

    @property
    def end_index(self):
        return self.content[-1].end_index

    #
    def __getitem__(self, item):
        return self.content[item]

    def __setitem__(self, index, value, style = None):
        self.content[index] = value

    def add_text(self, text, position=None, style=None):
        message = {'insertText': {'text': text,
                                         }}
        if position:
            message['insertText']['location'] = {
                "index": position
            }
        else:
            message['insertText']['endOfSegmentLocation'] = {}
        self._document._mutation([message])
        if style:
            updated = self._document.flush()[-1]
            print(updated)




    def style(self, text):
        message = {"updateTextStyle": {
            "objectId": self.table_id,
            "cellLocation": self.cell_location,
            "style":
                {
                    "fontSize":
                        {"magnitude": font_size,
                         "unit": "PT"}


                },
            "textRange": {
                "type": "ALL"
            },
            "fields": "fontSize"
        }
        }