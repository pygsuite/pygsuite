from pygsuite.docs.body import Body
from pygsuite.docs.footers import Footers
from pygsuite.docs.footnotes import Footnotes
from pygsuite.docs.headers import Headers


class Document:
    def __init__(self, id=None, name=None, client=None, _document=None):
        from pygsuite import Clients

        client = client or Clients.docs_client
        self.service = client
        self.id = id
        self._document = _document or client.documents().get(documentId=id).execute()
        self._change_queue = []

    def id(self):
        return self._document["id"]

    def _mutation(self, reqs, flush=False):
        if not reqs:
            return None
        self._change_queue += reqs
        if flush:
            return self.flush()

    def flush(self):
        if self._change_queue:
            out = (
                self.service.documents()
                .batchUpdate(body={"requests": self._change_queue}, documentId=self.id)
                .execute()["replies"]
            )
        else:
            return []
        self._change_queue = []
        self.refresh()
        return out

    # def delete(self, start=0, end=None, flush=True):
    #     end = end or self.body.end_index
    #     self._mutation([{'deleteContentRange': {'range': {
    #         "segmentId": None,
    #         "startIndex": start,
    #         "endIndex": end
    #     }}}])
    #     if flush:
    #         self.flush()

    @property
    def body(self):
        return Body(self._document.get("body"), self)

    @property
    def footers(self):
        return [Footers(item, self._sheet) for item in self._sheet.footers()]

    @property
    def footnotes(self):
        return [Footnotes(item, self._sheet) for item in self._sheet.footnotes()]

    @property
    def headers(self):
        return [Headers(item, self._sheet) for item in self._sheet.headers()]

    @property
    def title(self):
        return self._document.get("title")

    @title.setter
    def title(self, x):
        raise NotImplementedError

    def refresh(self):
        self._sheet = self.service.documents().get(documentId=self.id).execute()
