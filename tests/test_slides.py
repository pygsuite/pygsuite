from pygsuite.slides import ShapeType, ElementProperties

BRIGHT_GREEN_HEX = "#72FF33"


def test_presentation(test_presentation):
    prez = test_presentation
    slide = prez.add_slide(flush=True)
    slide.add_shape(
        ShapeType.TEXT_BOX, ElementProperties(x=0, y=0, height=50, width="100%")
    ).text = "test"
    prez.flush()
    assert prez[1].shapes[0].text.strip() == "test"


def test_layouts(test_presentation):

    deck = test_presentation
    print(deck.layouts)
    test_layout = deck.layouts["Title slide"]

    for element in test_layout.elements:
        print(element)

    deck.add_slide(
        layout=deck.layouts["Title slide"],
        index=0,
        placeholders={"CENTERED_TITLE": """ TEST_PREZ""", "SUBTITLE": "SUB_TITLE"},
    )
    deck.flush(reverse=True)
    assert deck[0].shapes[0].text.strip() == "TEST_PREZ"
