# Drive

The `Drive` object can be used to quickly find and copy files.

<!-- prettier-ignore-start -->
!!! warning
    This object is due for deprecation in the near future. Please consider searching for
    files [using the `Folder` object]() instead, and [using the `File` object]() to create and copy files.
<!-- prettier-ignore-end -->

## Find files

You can search for a file or set of files by specifying the file name, and parent folder ID:

```python
from pygsuite import Drive

files = Drive.find_files(
    folder_id="1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la",
    name="Important Report",
)

for file in files:
    print(file.url)
```

### Find files by name matching

You can also use a looser match on name by setting `exact_match` to `False`, returning partial matches as well:

```python hl_lines="6"
from pygsuite import Drive

files = Drive.find_files(
    folder_id="1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la",
    name="Proposal",
    exact_match=False,
)

for file in files:
    print(file.url)
```

### Find files by type

You can specify the type of the file you are looking for with the `type` parameter:

```python hl_lines="2 7"
from pygsuite import Drive
from pygsuite.enums import MimeType

files = Drive.find_files(
    folder_id="1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la",
    name="Important Report",
    type=MimeType.SHEETS,
)

for file in files:
    print(file.url)
```

The `type` can be given directly as a string [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) name, or using the `MimeType` enumeration, which includes a host of common MIME types (e.g. `SHEETS`, `DOCS`, `SLIDES`, `PDF`, `JPEG`, `MS_EXCEL`, etc.).

### Search outside your Drive

You can include folders in your search that exist outside your `My Drive`, by setting `support_all_drives` to `True`:

```python hl_lines="6"
from pygsuite import Drive

files = Drive.find_files(
    folder_id="1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la",
    name="Team Feedback",
    support_all_drives=True,
)

for file in files:
    print(file.url)
```

<!-- prettier-ignore-start -->
!!! tip
    The more places Google Drive has to search, the slower this call can become.
    For this reason, only set this parameter to `True` if you know the file lives outside your Drive.
<!-- prettier-ignore-end -->

## Copying files

You can create a copy of a file by specifying the ID of the file to copy, the title of the new file,
and the folder ID to store the new file:

```python
from pygsuite import Drive

copy = Drive().copy_file(
    file_id="1aquE36j6iytch4nlJXdwC_yDrCAYyyvHho5DrYbPGqE",
    title="Copy of My Document",
    folder_id="1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la",
)

print(copy.get("id"))
```
