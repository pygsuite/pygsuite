from pygsuite import Clients, DefaultFonts, Document, TextStyle, Color
from analytics_utility_core.secrets import secret_store

BRIGHT_GREEN_HEX = '#3437eb'

if __name__ == "__main__":
    auth = secret_store["bi-gsuite-automation"]

    Clients.authorize_string(auth)

    document = Document(id="1l9jF432quDMVvOujDMhBgfn-HZkLOXN9GMcCi-SIekg")
    for object in document.body.content:
        print(object)
        print(object.start_index)
        print(object.end_index)
        print(getattr(object, "text", None))
    document.body.delete()
    document.body.add_text("ABC123", style=TextStyle(font_size=8, font_weight=200, color=Color(hex=BRIGHT_GREEN_HEX)))
    # https://docs.google.com/feeds/download/documents/export/Export?id=1l9jF432quDMVvOujDMhBgfn-HZkLOXN9GMcCi-SIekg&exportFormat=png

    document.body.add_image(
        "https://cdn.pixabay.com/photo/2014/04/22/22/03/tiger-330148_960_720.jpg"
    )
    document.body.add_text("DEF\n\n", style=DefaultFonts.title)
    document.flush()