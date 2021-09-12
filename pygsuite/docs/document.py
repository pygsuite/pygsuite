from googleapiclient.errors import HttpError

from pygsuite import Clients
from pygsuite.common.drive_object import DriveObject
from pygsuite.common.parsing import parse_id
from pygsuite.docs.body import Body
from pygsuite.docs.footers import Footers
from pygsuite.docs.footnotes import Footnotes
from pygsuite.docs.headers import Headers
from pygsuite.enums import FileTypes
from pygsuite.utility.decorators import retry


class Document(DriveObject):
    """A document on google drive. """

    file_type = FileTypes.DOCS

    def __init__(self, id=None, name=None, client=None, _document=None, local=False):

        if not local:
            client = client or Clients.docs_client
        self.service = client
        DriveObject.__init__(self, id=parse_id(id) if id else None, client=client)
        self._document = _document or client.documents().get(documentId=self.id).execute()
        self._change_queue = []
        self.auto_sync = False

    @classmethod
    def create_new(cls, title: str, client=None):
        client = client or Clients.docs_client
        body = {"title": title}
        new = client.documents().create(body=body).execute()
        return Document(id=new.get("documentId"), client=client)

    def id(self):
        return self._document["id"]

    def _mutation(self, reqs, flush=False):
        if not reqs:
            return None
        self._change_queue += reqs
        if flush or self.auto_sync:
            return self.flush()

    @retry(HttpError, tries=3, delay=5, backoff=3)
    def flush(self, reverse=False):
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
        return [Footers(item, self) for item in self._document.get("footers")]

    @property
    def footnotes(self):
        return [Footnotes(item, self) for item in self._document.get("footnotes")]

    @property
    def headers(self):
        return [Headers(item, self) for item in self._document.get("headers")]

    @property
    def title(self):
        return self._document.get("title")

    @title.setter
    def title(self, title: str):
        raise NotImplementedError

    def refresh(self):
        self._document = self.service.documents().get(documentId=self.id).execute()
        self.body._pending = []

    @property
    def url(self):
        return f"https://docs.google.com/docs/d/{self.id}"
