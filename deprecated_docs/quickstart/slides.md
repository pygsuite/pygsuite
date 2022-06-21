## Setup

This quickstart assumes that you have already created an auth object using the auth quickstart.

Authorization is the same for all examples.

### Basic

This example walks through how to add slides to a deck.

#### Setup

Define a hex constant color and import some useful files.

Then create a blank slideshow and copy the URL into the TEST_SLIDES constant.

```python
from pygsuite import Clients, DefaultFonts, Document, TextStyle, Color

BRIGHT_GREEN_HEX = '#72FF33'

TEST_SLIDES = r'https://docs.google.com/document/d/############/edit'

```

#### Authorize Clients

Pass in the auth object you generated from the auth quickstart.

```python
Clients.authorize(AUTH_PLACEHOLDER)
```

#### Create Slides Object

Create the slide object, then clear it to have a blank slate.

```python
from pygsuite import Presentation
prez = Presentation(id='https://docs.google.com/presentation/d/1fkEmiaeQ256sfGJnCwEHHr46bQxn3VNdqedBDochjBc/edit#slide=id.p')
```

### Check Out Our Templates

An easy way to create content in slides is through filling in the default templates.

You can loop through and print them. This tutorial assumes you created an empty
deck off the default template.

```python
for layout in prez.layouts:
    print(layout)
```

Seems like we've got some useful templates there!

Titles and big numbers are always useful. Let's see what details they have.

```python
title_layout = prez.layouts["Title slide"]
for element in title_layout.placeholders:
    print(element)

number_layout = prez.layouts["Big number"]
for element in number_layout.placeholders:
    print(element)

```

#### Add Content

We can use those placeholders to quickly add content to our deck.

Let's add a title slide and a countdown from 5 to 1.

To do this, we'll reference the layouts, and pass them values to populate into the placeholders we
identified earlier.

First, the title:

```python
prez.add_slide(
    layout=prez.layouts["Title slide"],
    index=0,
    placeholders={
        "CENTERED_TITLE": """My Awesome Countdown""",
        "SUBTITLE": "Powered by Pygsuite"
    },
)
```

Then we can loop through the countdown to add our slides.

```python
for idx in reversed(range(1, 5)):
    prez.add_slide(
        layout=prez.layouts["Big number"],
        placeholders={
            "TITLE": str(idx),
            "BODY": 'Zero!' if idx ==0 else '...'
        },
    )
```

#### Flushing

This hasn't actually changed our presentation at all!

To actually commit the changes, we need to _flush_ them to google.

This will add them all into one batch request and submit them to google.

This is the default behavior because Google's APIs are slow and full of quotas - it's almost
always optimal to write out your logic in a clear way, then flush out the changes in a
single large batch to google.

Pygsuite does support auto-flushing on every operation if you prefer. See the
advanced configuration for details.

But to make our changes live, we just need to run one call.

```python
prez.flush()
```

### Entire script

```python
from pygsuite import Presentation

prez = Presentation(id='https://docs.google.com/presentation/d/1fkEmiaeQ256sfGJnCwEHHr46bQxn3VNdqedBDochjBc/edit#slide=id.p')


for layout in prez.layouts:
    print(layout)

title_layout = prez.layouts["Title slide"]
for element in title_layout.placeholders:
    print(element)

number_layout = prez.layouts["Big number"]
for element in number_layout.placeholders:
    print(element)

prez.add_slide(
    layout=prez.layouts["Title slide"],
    placeholders={
        "CENTERED_TITLE": """My Awesome Countdown""",
        "SUBTITLE": "Powered by Pygsuite"
    },
)


for idx in reversed(range(0, 5)):
    prez.add_slide(
        layout=prez.layouts["Big number"],
        placeholders={
            "TITLE": str(idx),
            "BODY": 'Zero!' if idx ==0 else '...'
        },
    )

prez.flush()
```
