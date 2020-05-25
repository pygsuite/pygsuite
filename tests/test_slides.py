from os import environ

from pygsuite import DefaultFonts, Document, TextStyle, Color

BRIGHT_GREEN_HEX = "#72FF33"


def test_presentation(test_presentation):
    document = Document(id=environ["TEST_DOCUMENT"])
    docbody = document.body
    docbody.delete()
    docbody.add_text(
        "Hello, World",
        style=TextStyle(font_size=18, font_weight=200, color=Color(hex=BRIGHT_GREEN_HEX)),
    )
    # image source: create commons: https://commons.wikimedia.org/wiki/File:Cisticola_exilis.jpg
    docbody.newline(count=2)
    docbody.add_text("A Report on Birds", style=DefaultFonts.TITLE)
    docbody.newline()
    docbody.add_image("https://upload.wikimedia.org/wikipedia/commons/0/0d/Cisticola_exilis.jpg")
    docbody.newline()
    docbody.add_text("Birds are a...", style=DefaultFonts.NORMAL_TEXT)
    document.flush()
