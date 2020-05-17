from pygsuite import Clients
from analytics_utility_core.secrets import secret_store
from pygsuite.slides import Presentation

if __name__ == "__main__":
    auth = secret_store["bi-gsuite-automation"]

    Clients.authorize_string(auth)

    deck = Presentation(id="1ziGoAi1n7tYEypapMWhTHJivklQjq5wI4xQcFlrrtzA")
    test_layout = deck.layouts["7.) Agenda Slide"]
    print(test_layout._layout)
    for element in test_layout.elements:
        print(element)

    print(test_layout.placeholders)

    deck.add_slide(
        layout=deck.layouts["7.) Agenda Slide"],
        index=0,
        placeholders={
            "BODY_2": """    1. Cost
    2. Adoption
    3. Others""",
            "TITLE_9": "April 21 2020",
        },
    )

    deck.add_slide(layout=deck.layouts["40.) Blank Slide"], placeholders={"TITLE": "Cost"}, index=0)
    deck.add_slide(
        layout=deck.layouts["40.) Blank Slide"], placeholders={"TITLE": "Adoption"}, index=0
    )
    deck.add_slide(
        layout=deck.layouts["40.) Blank Slide"],
        placeholders={"TITLE": "Performance Tracking"},
        index=0,
    )
    deck.add_slide(
        layout=deck.layouts["40.) Blank Slide"], placeholders={"TITLE": "Other Updates"}, index=0
    )
    deck.flush(reverse=True)

    #
    # print(document._document)
    # print(document.body.content)
    # print(vars(document._document))from pygsuite import Clients
    # from analytics_utility_core.secrets import secret_store
    # from pygsuite.docs import Document
    #
    # if __name__ == "__main__":
    #     auth = secret_store['bi-drive-automation']
    #
    #     Clients.authorize_string(auth)
    #
    #     document = Document(id = '1kJh3tPyXoDzu_TIltDAXHRiFj-X0XDlVUiOP0wz_M8E')
    #     print(document._document)
    #     print(document.body.content)
    #     # print(vars(document._document))
