from .slide import Slide
from .layout import Layout
from main.common.decorators import retry
from googleapiclient.errors import HttpError

class Presentation():
    def __init__(self, service, id):
        self.service = service
        self.id = id
        self._presentation = service.presentations().get(
            presentationId=id).execute()
        self._change_queue = []

    @retry((HttpError), tries = 3, delay =10, backoff = 5)
    def flush(self):
        out = self.service.presentations().batchUpdate(body={'requests': self._change_queue},
                                                              presentationId=self.id).execute()['replies']

        self._change_queue = []
        self.refresh()
        return out


    def refresh(self):
        self._presentation = self.service.presentations().get(
            presentationId=self.id).execute()

    @property
    def slides(self):
        return [Slide(slide, self) for slide in self._presentation.get('slides')]

    def get_slide(self, id):
        return Slide.from_id(id, self)

    @property
    def layouts(self):
        return [Layout(layout, self) for layout in self._presentation.get('layouts')]

    def _mutation(self, reqs, flush=False):
        if not reqs:
            return None
        self._change_queue += reqs
        if flush:
            return self.flush()

    def add_slide(self, ref=None, placeholders = None):
        base = {}
        if ref:
            base['slideLayoutReference'] = {'layoutId': ref}
        reqs = [
            {'createSlide': base}
        ]
        # return added slide ID
        return self._mutation(reqs)[0]['createSlide']['objectId']
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
