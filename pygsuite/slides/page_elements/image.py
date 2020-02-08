from .base_element import BaseElement

CENTER_INSIDE = 'CENTER_INSIDE'
CENTER_CROP = 'CENTER_CROP'

class Image(BaseElement):
    def __init__(self, element, presentation):
        BaseElement.__init__(self, element, presentation)
        self._element = element
        self._presentation = presentation
        self._details = self._element.get('image')
        self.text = None


    @property
    def id(self):
        return self._element['objectId']


    @property
    def position(self):
        return (self._element['transform']['scaleX'], self._element['transform']['scaleY'])

    def delete(self):
        reqs = [
            {'deleteObject': {'objectId': self.id}},
        ]
        self._presentation._mutation(reqs)

    def update_image(self, new_url, replace_method = CENTER_INSIDE):
        reqs = [{
            'replaceImage': {
                "imageObjectId": self.id,
                "imageReplaceMethod": replace_method,
                "url": new_url
            }
        },
          ]

        return self._presentation._mutation(reqs)