from typing import Dict, Union, Optional, Any

from googleapiclient.errors import HttpError

from pygsuite import Clients
from pygsuite.common.parsing import parse_id
from pygsuite.drive.drive_object import DriveObject
from pygsuite.enums import MimeType
from pygsuite.utility.decorators import retry
from .layout import Layout
from .slide import Slide


class Presentation(DriveObject):

    _mimetype = MimeType.SLIDES
    _base_url = "https://docs.google.com/presentation/d/{}/edit"

    def __init__(self, id, client=None):
        self.service = client or Clients.slides_client
        self.id = parse_id(id) if id else None
        DriveObject.__init__(self, id=id, client=client)

        self._presentation = self.service.presentations().get(presentationId=self.id).execute()
        self._change_queue = []

    def __getitem__(self, item) -> Slide:
        return self.slides[item]

    def __setitem__(self, index, value: Slide, style=None):
        self._mutation([{"slideObjectIds": [Slide.id], "insertionIndex": index}])
        self.flush()

    @retry((HttpError), tries=3, delay=5, backoff=3)
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
            self.service.presentations()
            .batchUpdate(body={"requests": final}, presentationId=self.id)
            .execute()["replies"]
        )

        self._change_queue = []
        self.refresh()
        return out

    def refresh(self):
        self._presentation = self.service.presentations().get(presentationId=self.id).execute()

    @property
    def slides(self):
        return [Slide(slide, self) for slide in self._presentation.get("slides")]

    def get_slide(self, id: str) -> Slide:
        return Slide.from_id(id, self)

    @property
    def layouts(self) -> Dict[str, Layout]:
        layouts = [Layout(layout, self) for layout in self._presentation.get("layouts")]
        return {layout.display_name: layout for layout in layouts}

    def _mutation(self, reqs, flush=False):
        if not reqs:
            return None
        self._change_queue += reqs
        if flush:
            return self.flush()

    @property
    def url(self):
        return f"https://docs.google.com/presentation/d/{self.id}"

    def add_slide(
        self,
        layout: Union[str, Layout] = None,
        placeholders: Dict = None,
        index: Optional[int] = None,
        flush: bool = False,
    ) -> Optional[Slide]:
        base: Dict[str, Any] = {}
        placeholder_mappings = []
        if layout:
            if isinstance(layout, Layout):
                id = layout.id
            else:
                id = layout
            base["slideLayoutReference"] = {"layoutId": id}
        if not index is None:  # noqa: E714
            base["insertionIndex"] = index
        if placeholders is not None:
            if not isinstance(layout, Layout):
                raise ValueError("Cannot pass placeholders without a reference layout!")
            placeholder_mappings = [
                layout.build_reference_map(key, val) for key, val in placeholders.items()
            ]
            base["placeholderIdMappings"] = [map[1] for map in placeholder_mappings]
        reqs = [{"createSlide": base}]
        base_idx = -1
        for map in placeholder_mappings:
            reqs.append(map[0])
            base_idx -= 1

        # return added slide ID
        # always flush
        out = self._mutation([reqs], flush=flush)
        if flush:
            return self.get_slide(out[base_idx]["createSlide"]["objectId"])
        return None
        # self.refresh()
        # return self.get_slide(created)


#     def replace(self, args):
#         reqs = [
#             {'replaceAllText': {
#                 'containsText': {'text': '{{NAME}}'},
#                 'replaceText': 'Hello World!'
#             }},
#             {'createImage': {
#                 'url': img_url,
#                 'elementProperties': {
#                     'pageObjectId': slide['objectId'],
#                     'size': obj['size'],
#                     'transform': obj['transform'],
#                 }
#             }},
#             {'deleteObject': {'objectId': obj['objectId']}},
#         ]
# SLIDES.presentations().batchUpdate(body={'requests': reqs},
#                                    presentationId=DECK_ID).execute()
