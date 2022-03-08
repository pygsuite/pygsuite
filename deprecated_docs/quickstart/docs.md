## Setup

This quickstart assumes that you have already authorized your client, per the auth quickstart.

Authorization is the same for all examples.

### Basic

This example walks through how to get a document and append text and images to it.

#### Setup

Define a hex constant color and import some useful files.

Then create a blank document and copy the URL into the TEST_DOCUMENT constant.

```python
from pygsuite import Clients, DefaultFonts, Document, TextStyle, Color

BRIGHT_GREEN_HEX = '#72FF33'

TEST_DOCUMENT = r'https://docs.google.com/document/d/############/edit'

```

#### Authorize Clients

Pass in the auth object you generated from the auth quickstart.

```python
Clients.authorize(AUTH_PLACEHOLDER)
```

#### Create Document Object

Create the document object, then clear it to have a blank slate.

```python
document = Document(id=TEST_DOCUMENT)
docbody = document.body
docbody.delete()
```

#### Add Content

Then we'll add content to it. The add_text method is your default for adding text. This example uses the
default position - none - to append to the end of the document. If you want to append to another position,
you can specify that.

To create custom styling, use a TextStyle object:

```python
TextStyle(font_size=18, font_weight=200, color=Color(hex=BRIGHT_GREEN_HEX))
```

To access the defaults, use the DefaultFonts enum.

```python
docbody.add_text("A Report on Birds", style=DefaultFonts.title)
```

When we're done with our content, call flush to update the document.

```python
docbody.add_text("Hello, World", style=TextStyle(font_size=18, font_weight=200, color=Color(hex=BRIGHT_GREEN_HEX)))

docbody.newline(count=2)
docbody.add_text("A Report on Birds", style=DefaultFonts.title)
docbody.newline()
# image source: create commons: https://commons.wikimedia.org/wiki/File:Cisticola_exilis.jpg
docbody.add_image(
    "https://upload.wikimedia.org/wikipedia/commons/0/0d/Cisticola_exilis.jpg"
)
docbody.newline()
docbody.add_text('Birds are a...', style=DefaultFonts.normal)
document.flush()

```

### Entire script

```python
from pygsuite import Clients, DefaultFonts, Document, TextStyle, Color
BRIGHT_GREEN_HEX = '#72FF33'

TEST_DOCUMENT = r'https://docs.google.com/document/d/############/edit'


document = Document(id=TEST_DOCUMENT)
docbody = document.body
docbody.delete()
docbody.add_text("Hello, World", style=TextStyle(font_size=18, font_weight=200, color=Color(hex=BRIGHT_GREEN_HEX)))

docbody.newline(count=2)
docbody.add_text("A Report on Birds", style=DefaultFonts.title)
docbody.newline()
# image source: create commons: https://commons.wikimedia.org/wiki/File:Cisticola_exilis.jpg
docbody.add_image(
    "https://upload.wikimedia.org/wikipedia/commons/0/0d/Cisticola_exilis.jpg"
)
docbody.newline()
docbody.add_text('Birds are a...', style=DefaultFonts.normal)
document.flush()


```
