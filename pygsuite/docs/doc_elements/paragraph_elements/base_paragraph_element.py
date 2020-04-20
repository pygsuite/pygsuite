
class BaseParagraphElement(object):
    def __init__(self, element:dict, document):
        self._element = element
        self._document = document

    def end_index(self):
        return self._element.get('endIndex')

    def start_index(self):
        return self._element.get('startIndex')
