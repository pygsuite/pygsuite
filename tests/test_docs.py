from os import environ

from pygsuite import DefaultFonts, Document, TextStyle, Color
from pygsuite.docs.doc_elements.paragraph import Paragraph

BRIGHT_GREEN_HEX = "#72FF33"


def test_text(test_document):
    document = test_document
    docbody = document.body
    docbody.delete()
    docbody.add_text(
        "TEST_CUSTOM\n",
        style=TextStyle(font_size=18, font_weight=200, color=Color(hex=BRIGHT_GREEN_HEX)),
    )
    docbody.add_text("TEST_DEFAULT\n", style=DefaultFonts.NORMAL_TEXT)

    docbody.add_text("TEST_INDEX\n", style=DefaultFonts.NORMAL_TEXT, position=1)
    document.flush()
    text = [item for item in document.body if isinstance(item, Paragraph)]
    assert text[0].text.strip() == "TEST_INDEX"
    assert text[2].text.strip() == "TEST_DEFAULT"
    # TODO: return style objects
    assert text[1].elements[0].style.font_size == 18


def test_paragraph(test_document):
    document = test_document
    docbody = document.body
    docbody.delete()
    docbody.add_text(
        "TEST_CUSTOM\n",
        style=TextStyle(font_size=18, font_weight=200, color=Color(hex=BRIGHT_GREEN_HEX)),
    )
    docbody.flush()
    docbody.content[1].text = "TEST_CUSTOM_SETTER"
    docbody.add_text("INSERT\n", position=0)
    docbody.flush()
    docbody.paragraphs[1].elements[0].style = TextStyle(
        font_size=24, font_weight=500, color=Color(hex=BRIGHT_GREEN_HEX)
    )
    docbody.flush()

    assert docbody.content[2].text.strip() == "TEST_CUSTOM_SETTER"
    assert docbody.paragraphs[1].elements[0].style.font_size == 24
