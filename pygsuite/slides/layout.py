from .page_element import PageElement

class Layout(object):
    def __init__(self, layout, presentation):
        self._layout=layout
        self._presentation = presentation

    @property
    def elements(self):
        return [PageElement(element, self._presentation) for element in self._layout.get('pageElements')]

    @property
    def layout_properties(self):
        return self._layout['layoutProperties']

    @property
    def display_name(self):
        return self.layout_properties['displayName']


    @property
    def id(self):
        return self._layout['objectId']