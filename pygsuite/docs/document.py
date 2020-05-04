from googleapiclient.errors import HttpError

from pygsuite.docs.body import Body
from pygsuite.docs.footers import Footers
from pygsuite.docs.footnotes import Footnotes
from pygsuite.docs.headers import Headers
from pygsuite.utility.decorators import retry


def parse_id(input_id: str) -> str:
    if "/" in input_id:
        portions = input_id.split("/")
        for idx, val in enumerate(portions):
            if val == "d":
                return portions[idx + 1]
        raise ValueError("Unable to parse ID from input")
    else:
        return input_id


class Document:
    def __init__(self, id=None, name=None, client=None, _document=None, local=False):
        from pygsuite import Clients

        if not local:
            client = client or Clients.docs_client
        self.service = client
        self.id = parse_id(id)
        self._document = _document or client.documents().get(documentId=self.id).execute()
        self._change_queue = []

    def id(self):
        return self._document["id"]

    def _mutation(self, reqs, flush=False):
        if not reqs:
            return None
        self._change_queue += reqs
        if flush:
            return self.flush()

    @retry((HttpError), tries=3, delay=10, backoff=5)
    def flush(self, reverse=False):
        print(self._change_queue)
        if reverse:
            base = reversed(self._change_queue)
        else:
            base = self._change_queue
        final = []
        for item in base:
            if isinstance(item, list):
                for i in item:
                    final.append(i)
            else:
                final.append(item)
        if not base:
            return []
        out = (
            self.service.documents()
            .batchUpdate(body={"requests": final}, documentId=self.id)
            .execute()["replies"]
        )

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
        self._document = self.service.documents().get(documentId=self.id).execute()
        self.body._pending = []
