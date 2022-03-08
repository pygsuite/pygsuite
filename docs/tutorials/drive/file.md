# Files

Using **pygsuite**, creating and manipulating Google Drive files is easy (and maybe even fun).

## Creating files

Creating a file in **pygsuite** is fast and simple:

```python
from pygsuite import File

my_file = File.create(name="My first file")
print(my_file.url)
```

### Specifying a folder location

You can add a list of parent folder IDs that will contain the new file:

```python hl_lines="5"
from pygsuite import File

my_file = File.create(
    name="My first file",
    parent_folder_ids=["1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la"],
)
print(my_file.url)
```

### Specifying a file type

Files of a given type can be created by providing the MIME type:

```python hl_lines="2 7"
from pygsuite import File
from pygsuite.enums import MimeType

my_file = File.create(
    name="My first spreadsheet",
    parent_folder_ids=["1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la"],
    type=MimeType.SHEETS,
)
print(my_file.url)
```

The `type` can be given directly as a string [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) name, or using the `MimeType` enumeration, which includes a host of common MIME types (e.g. `SHEETS`, `DOCS`, `SLIDES`, `PDF`, `JPEG`, `MS_EXCEL`, etc.).

### Specifying content in the file

To create a non-empty file, the content of the file can be provided as a [`MediaFileUpload`](), [`MediaIoBaseUpload`](), or simply bytes of the object (`BytesIO`). This can be especially useful for saving objects (e.g. images, data) that are stored in Python's memory to a Google Drive location:

```python hl_lines="6 7 11 12"
from io import BytesIO
import requests

from pygsuite import File

response = requests.get("https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg")
image_in_bytes = BytesIO(response.content)

new_file = File.create(
    name="Google Logo",
    mimetype=MimeType.SVG,
    media_body=image_in_bytes,
)

print(new_file.url)
```

## Uploading files

A common way to create a new Google Drive file is to upload a local file, or one existing in memory.

```python
from pygsuite import File
from pygsuite.enums import MimeType

text_file = File.upload(
    filepath="/path/to/file.txt",
    name="My Text File",
    mimetype=MimeType.PLAIN_TEXT,
)

print(text_file.url)
```

### Specifying an upload location

Uploading files shares many of the same options with creating files, such as specifying the upload location(s):

```python hl_lines="7"
from pygsuite import File
from pygsuite.enums import MimeType

text_file = File.upload(
    filepath="/path/to/file.txt",
    name="My Text File",
    parent_folder_ids=["1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la"],
    mimetype=MimeType.PLAIN_TEXT,
)

print(text_file.url)
```

### Converting to Google

Converting a file to a Google Document format can be handy when uploading files that will later be used in Google Drive.
For instance, if you want to upload an Excel file and simultaneously convert it to a Google Sheet:

```python hl_lines="2 8"
from pygsuite import File
from pygsuite.enums import MimeType, GoogleDocFormat

new_sheets = File.upload(
    filepath="/path/to/file.xlsx",
    name="My Spreadsheet",
    mimetype=MimeType.MS_EXCEL,
    convert_to=GoogleDocFormat.SHEETS,
)

print(new_sheets.url)
```

## Fetching files

Commonly, you may want to "get or create" a file&mdash;this can be achieved using the `get_safe` method, in which a new file is created if a matching one cannot be found:

```python
from pygsuite import File
from pygsuite.enums import MimeType

new_or_existing = File.get_safe(
    name="My Spreadsheet",
    parent_folder_ids=["1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la"],
    mimetype=MimeType.MS_EXCEL,
)

print(new_or_existing.url)
```

<!-- prettier-ignore-start -->
!!! tip
    To confirm if a new file has been created in the `get_safe` process, look to your logs!
    If so, you will see something like this: `No matching file found, creating file now...`
<!-- prettier-ignore-end -->

## Copying files

Coming soon!

## Moving files

Move files in Google Drive easily by specifying the new destination(s) of the file:

```python hl_lines="5 6 7"
from pygsuite import File

my_file = File.create(name="My first file")

my_file.move(
    destination_folder_ids=["1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la"],
)
```

## File metadata

By default, you can access key pieces of metadata about a file:

```python
from pygsuite import File

my_file = File.create(name="My first file")

print(my_file.id)
print(my_file.kind)
print(my_file.name)
print(my_file.mimetype)
print(my_file.url)
```

### Getting additional metadata

Other information about a file can be fetched for a given file:

```python hl_lines="4"
from pygsuite import File

my_file = File.create(name="My first file")
created_time = my_file.fetch_metadata(fields=["createdTime"]).get("createdTime")
print(created_time)
```

<!-- prettier-ignore-start -->
!!! tip
    For a full list of what fields are available, review [the Google documentation](https://developers.google.com/drive/api/v3/reference/files).
<!-- prettier-ignore-end -->

### Get _all_ metadata

You can also fetch all metadata available for a file, though it won't necessarily be your fastest API call:

```python hl_lines="4"
from pygsuite import File

my_file = File.create(name="My first file")
metadata = my_file.fetch_metadata(fields=["*"])
print(metadata)
```

## File comments

View comments data for a given file:

```python hl_lines="9 10"
from pygsuite import File
from pygsuite.enums import MimeType

team_document = File.get_safe(
    name="Project Brief",
    mimetype=MimeType.DOCS,
)

for comment in team_document.comments:
    print(comment)
```

## File sharing

You can update the sharing permissions on your file:

```python hl_lines="2 5 6 7 8"
from pygsuite import File
from pygsuite.enums import PermissionType

my_file = File.create(name="Vacation Ideas")
my_file.share(
    role=PermissionType.READER,
    user="spouse@gmail.com",
)
```

### Share with everyone

Make a file accessible by anyone with a link (careful with this one at work!):

```python hl_lines="7"
from pygsuite import File
from pygsuite.enums import PermissionType

my_file = File.create(name="Vacation Ideas")
my_file.share(
    role=PermissionType.READER,
    anyone=True,
)
```

## Downloading files

Coming soon!

## Deleting files

Permanently delete a given file:

```python hl_lines="4"
from pygsuite import File

short_lived = File.create(name="Ephemeral File")
short_lived.delete()
```
