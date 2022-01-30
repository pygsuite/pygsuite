<img src="./images/pygsuite_logo.png" width=20% height=20%>

# pygsuite

A pythonic library for interacting with Google Suite products through a convenient,
object-oriented model.

It currently includes support for working with the following GSuite offerings. 

- Sheets
- Drive
- Slides
- Drive

## Overview

Pygsuite is a light, pythonic wrapper around the core Google provided API clients. It offers efficient APIs for batch requests to automate the creation, manipulation, and management of GSuite content. 

Pygsuite's code is hosted on GitHub.

You can read more about the raw GSuite APIs here [here](https://developers.google.com/gsuite/aspects/apis).

## Install

`pygsuite` is [hosted on PyPI](https://pypi.org/project/pygsuite/), and is installable with [pip](https://pip.pypa.io/en/stable/):

```bash
$ pip install pygsuite
```

To use the image upload helpers in `pygsuite`, use the `images` optional installation extras:

```bash
$ pip install pygsuite[images]
```

## Want to dive right in?

Get started with the quickstart examples. You'll need to start with the auth quickstart to use any of them, so begin there.

- [Auth](./quickstart/auth.md)
- [Sheets](./quickstart/sheets.md)
- [Docs](./quickstart/docs.md)
- [Slides](./quickstart/slides.md)
- [Drive]('./quickstart/drive.md)

## More Information

Refer to the [goals](./goals.md) and [features](./features.md) pages for overviews of the package.

The [quickstart](./quickstart/auth.md) pages will let you dive right in and start writing code. 

The [examples](./ref_examples/examples.md) page will walk you through more complicated
examples that highlight more complex features of each module
and how they can interact.

The [reference](./reference/reference.md) section will provide detailed reference
examples for specific use cases.

The [api](./api/api.md) section will give you details on each of the base
python classes. 