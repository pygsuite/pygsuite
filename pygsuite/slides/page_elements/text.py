class BaseTextElement(object):
    def __init__(self, element, presentation):
        self._element = element
        self._presentation = presentation

    def end_index(self):
        return self._element.get("endIndex")

    def start_index(self):
        return self._element.get("startIndex")

    def text_run(self):
        return self._element.get("textRun")


class TextRun(BaseTextElement):
    def __init__(self, element, presentation):
        BaseTextElement.__init__(self, element, presentation)
        self._detail = element.get("textRun")

    @property
    def content(self):
        return self._detail.get("content")

    def style(self):
        return self._detail.get("style")


class ParagraphMarker(BaseTextElement):
    def __init__(self, element, presentation):
        BaseTextElement.__init__(self, element, presentation)
        self._detail = element.get("paragraphMarker")

    def style(self):
        return self._detail.get("style")

    def bullet(self):
        return self._detail.get("bullet")


""""textElements": [ {
    "endIndex": 224,
    "paragraphMarker": { "style": {} }
  }, {
    "endIndex": 130,
    "textRun": { "content": "Li lingues differe in li grammatica e li vocabules. Omnicos directe al desirabilite de un nov ", "style": {} }
  }, {
    "endIndex": 143,
    "startIndex": 130,
    "textRun": { "content": "lingua franca", "style": { "italic": True } }
  }, {
    "endIndex": 224,
    "startIndex": 143,
    "textRun": { "content": ": solmen va esser necessi far:\n", "style": {} }
  }, {
    "endIndex": 243,
    "startIndex": 224,
    "paragraphMarker": {
      "style": { "indentStart": { "magnitude": 36, "unit": "PT" }, "direction": "LEFT_TO_RIGHT", "indentFirstLine": { "magnitude": 18, "unit": "PT" }, "spacingMode": "COLLAPSE_LISTS" },
      "bullet": { "listId": "foo123", "glyph": "\u25cf" }
    }
  }, {
    "endIndex": 243,
    "startIndex": 224,
    "textRun": { "content": "uniform grammatica\n", "style": {} }
  }, {
    "endIndex": 257,
    "startIndex": 243,
    "paragraphMarker": {
        "style": { "indentStart": { "magnitude": 36, "unit": "PT" }, "direction": "LEFT_TO_RIGHT", "indentFirstLine": { "magnitude": 18, "unit": "PT" }, "spacingMode": "COLLAPSE_LISTS" },
        "bullet": { "listId": "foo123", "glyph": "\u25cf" }
    }
}, {
    "endIndex": 257,
    "startIndex": 243,
    "textRun": { "content": "Pronunciation\n", "style": {} }
}, {
    "endIndex": 277,
    "startIndex": 257,
    "paragraphMarker": {
        "style": { "indentStart": { "magnitude": 36, "unit": "PT" }, "indentFirstLine": { "magnitude": 18, "unit": "PT" }, "spacingMode": "COLLAPSE_LISTS" },
        "bullet": { "listId": "foo123", "glyph": "\u25cf" }
    }
}, {
    "endIndex": 277,
    "startIndex": 257,
    "textRun": { "content": "plu sommun paroles.\n", "style": {} }
}, {
    "endIndex": 500,
    "startIndex": 277,
    "paragraphMarker": { "style": {} }
}, {
    "endIndex": 500,
    "startIndex": 277,
    "textRun": { "content": "Ka swu thefognay, tay waddeant varpa u inzo.\n", "style": {} }
}]"""
