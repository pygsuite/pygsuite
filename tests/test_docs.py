from os import environ

from pygsuite import DefaultFonts, Document, TextStyle, Color
from pygsuite.docs.doc_elements.paragraph import Paragraph

BRIGHT_GREEN_HEX = "#72FF33"


def test_text(auth_test_clients):
    document = Document(id=environ["TEST_DOCUMENT"])
    docbody = document.body
    docbody.delete()
    docbody.add_text(
        "TEST_CUSTOM\n",
        style=TextStyle(font_size=18, font_weight=200, color=Color(hex=BRIGHT_GREEN_HEX)),
    )
    docbody.add_text("TEST_DEFAULT\n", style=DefaultFonts.normal)

    docbody.add_text("TEST_INDEX\n", style=DefaultFonts.normal, position=1)
    document.flush()
    text = [item for item in document.body if isinstance(item, Paragraph)]
    assert text[0].text.strip() == "TEST_INDEX"
    assert text[2].text.strip() == "TEST_DEFAULT"
    # TODO: return style objects
    assert text[1].elements[0].style["fontSize"] == {"magnitude": 18, "unit": "PT"}
