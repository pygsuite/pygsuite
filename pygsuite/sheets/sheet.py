from .worksheet import Worksheet

class Spreadsheet():
    def __init__(self, service, id):
        self.service = service
        self.id = id
        self._sheet = service.open_by_key(id)
        self._change_queue = []

    def id(self):
        return self._sheet['id']

    def flush(self):
        out = self.service.presentations().batchUpdate(body={'requests': self._change_queue},
                                                       presentationId=self.id).execute()['replies']
        self._change_queue = []
        self.refresh()
        return out

    @property
    def worksheets(self):
        return [Worksheet(item, self._sheet) for item in self._sheet.worksheets()]

    def __getitem__(self, item):
        return self.worksheets[item]

    def refresh(self):
        self._sheet = self.service.open_by_key(self.id)

