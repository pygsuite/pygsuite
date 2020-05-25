from pygsuite import Clients, DefaultFonts, Document, TextStyle, Color
from analytics_utility_core.secrets import secret_store
from time import sleep

BRIGHT_GREEN_HEX = '#72FF33'

TEST_DOCUMENT = r'https://docs.google.com/document/d/1FjTc0r2D9Ck8V2gkHxDsR11TaC0rM_NKN6_qopKYFDQ/edit'

if __name__ == "__main__":
    auth = secret_store["bi-gsuite-automation"]

    Clients.authorize_string(auth)

    document = Document(id=TEST_DOCUMENT)
    docbody = document.body
    docbody.delete()
    docbody.add_text("Hello, World", style=TextStyle(font_size=18, font_weight=200, color=Color(hex=BRIGHT_GREEN_HEX)))
    # image source: create commons: https://commons.wikimedia.org/wiki/File:Cisticola_exilis.jpg
    docbody.newline(count=2)
    docbody.add_text("A Report on Birds", style=DefaultFonts.title)
    docbody.newline()
    docbody.add_image(
        "https://upload.wikimedia.org/wikipedia/commons/0/0d/Cisticola_exilis.jpg"
    )
    docbody.newline()
    docbody.add_text('Birds are a...', style=DefaultFonts.normal)
    document.flush()
    for item in document.body:
        print(item)