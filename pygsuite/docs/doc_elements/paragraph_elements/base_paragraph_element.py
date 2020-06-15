class BaseParagraphElement(object):
    def __init__(self, element: dict, document):
        self._element = element
        self._document = document

    @property
    def start_index(self) -> int:
        return self._element.get("startIndex")

    @property
    def end_index(self) -> int:
        return self._element.get("endIndex")
