from googleapiclient.errors import HttpError

from pygsuite import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.drive.drive_object import DriveObject
from pygsuite.enums import MimeType
from pygsuite.utility.decorators import retry
from .form_settings import FormSettings
from .item import Item

class Form(DriveObject):
    """A form on google drive."""

    _mimetype = MimeType.FORMS

    def __init__(self, id: str = None, client=None, name=None, _form=None, local: bool = False):

        if not local:
            client = client or Clients.forms_client
        self.service = client
        self.id = parse_id(id) if id else None
        DriveObject.__init__(self, id=id, client=client)
        self._form = _form or client.forms().get(formId=self.id).execute()
        self._change_queue = []
        self.auto_sync = False

    def id(self):
        return self._form["id"]

    def _mutation(self, reqs, flush:bool=False):
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
        print(final)
        out = (
            self.service.forms()
                .batchUpdate(body={"requests": final}, formId=self.id)
                .execute()["replies"]
        )

        self._change_queue = []
        self.refresh()
        return out

    @property
    def items(self):
        return [Item(item, self, idx) for idx, item in enumerate(self._form.get('items',[]))]

    # def delete(self, start=0, end=None, flush=True):
    #     end = end or self.body.end_index
    #     self._mutation([{'deleteContentRange': {'range': {
    #         "segmentId": None,
    #         "startIndex": start,
    #         "endIndex": end
    #     }}}])
    #     if flush:
    #         self.flush()

    def refresh(self):
        self._form = self.service.forms().get(formId=self.id).execute()

    @property
    def url(self):
        return f"https://drive.google.com/forms/d/{self.id}"
