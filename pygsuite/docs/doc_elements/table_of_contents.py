from pygsuite.docs.doc_elements import BaseElement


class TableOfContents(BaseElement):
    def __init__(self, element, document, last):
        BaseElement.__init__(self, element=element, document=document, last=last)
        self._paragraph = self._element.get("table_of_contents")

    @property
    def section_style(self):
        return self._element.get("sectionStyle")

    def delete(self):
        if not self.start_index:
            return
        if self.start_index == self.end_index:
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
