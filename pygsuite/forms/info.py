'''{
  "title": string,
  "documentTitle": string,
  "description": string
}'''


class Info(object):
    def __init__(self, info: dict, form):
        # TODO
        self._info = info
        self._form = form

    @property
    def title(self):
        return self._info.get('title')

    @property
    def description(self):
        return self._info.get('description')

    @property
    def document_title(self):
        return self._info.get('document_title')
