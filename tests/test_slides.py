from os import environ
from pygsuite import Clients, Spreadsheet, Presentation
from pygsuite.slides import ShapeType, ElementProperties

from pygsuite import DefaultFonts, Document, TextStyle, Color

BRIGHT_GREEN_HEX = "#72FF33"


def test_presentation(test_presentation):
    prez = test_presentation
    slide = prez.add_slide(flush=True)
    slide.add_shape(
        ShapeType.TEXT_BOX, ElementProperties(x=0, y=0, height=50, width="100%")
    ).text = "test"
    prez.flush()
    assert prez[1].shapes[0].text.strip() == "test"
