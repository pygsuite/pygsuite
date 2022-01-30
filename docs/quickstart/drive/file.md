_This quickstart assumes that you have already authorized your client, per the [auth quickstart](./auth.md). Authorization is the same for all examples._


# The File object

The `File` object represents one of the most atomic units of Google Drive. Files can be created, copied, moved, shared, downloaded, deleted, and more, mimicking actions available in the Google Drive UI.

## Creating files

### Creating empty files

Let's start with a simple example creating an empty text file in Google Drive:

```python
from pygsuite.drive import File


text_file = File.create(
    name="Empty Text File",
    mimetype="text/plain",
)

print(text_file.id)
```

Notice that we have given our file a name, and told the API what type of file we would like to create. The _type_ of the file is specified by a MIME type ([_Multipurpose Internet Mail Extensions_](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) for long). See [this reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types) or many other internet resources for information on common MIME types.

More often, however, we will likely be creating files with some content, either from an upload or from information stored in Python's memory.

### Creating files with content from memory

Oftentimes, we might want to take data we have stored in Python's memory, and create a Google Drive file with this content. For instance, we may have stored some text data that we want to insert into a newly created Google Doc, or we may want to save an image or PDF we have generated within Python as a file in Drive.

As an example, we can fetch an image from a URL, convert the image into bytes, and then create a new image file in Drive from the bytes we extract:

```python
from io import BytesIO
import requests

from pygsuite.drive import File


response = requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1280px-SNice.svg.png")
image_bytes = BytesIO(response.content)

image_file = File.create(
    name="Test Smiley",
    mimetype="image/png",
    media_body=image_bytes,
)

print(image_file.id)
```

Now if we login to Google Drive, we see our newly created PNG image file.

### Uploading files

The last way we may commonly create new Google Drive files is by uploading existing files on a local system. For this method, we can simply use a filepath to the file we would like to upload, as well as an option to convert the file to a Google Doc format, such as a Google Sheet or Google Doc:

```python
from pygsuite.drive import File
from pygsuite.enums import GoogleDocFormat


upload_file = r"examples\data\test data.xlsx"

sheets_file = File.upload(
    filepath=upload_file,
    name="Test Excel Upload",
    convert_to=GoogleDocFormat.SHEETS,
)

print(sheets_file.id)
```

In this upload example, we've taken an Excel file (`.xlsx`) that we have locally, and uploaded it into Google Drive. Along the way, we've used the optional `convert_to` parameter to specify that we want to convert this Excel file into a Google Sheet (specified by the type, `GoogleDocFormat.SHEETS`).

Currently, some common, supported conversions available include:

| From                                                            | To                                      |
|-----------------------------------------------------------------|-----------------------------------------|
| Microsoft Word, OpenDocument Text, HTML, RTF, plain text        | Google Docs                             |
| Microsoft Excel, OpenDocument Spreadsheet, CSV, TSV, plain text | Google Sheets                           |
| Microsoft Powerpoint, OpenDocument Presentation                 | Google Slides                           |
| JPEG, PNG, GIF, BMP, PDF                                        | Google Docs (embeds the image in a Doc) |
| plain text (special MIME type), JSON                            | Google Apps Scripts                     |

## Copying files

Coming soon!

## Moving files

Coming soon!

## Accessing file data

Google Drive files have specific metadata associated with them, including basic information such as the `name`, `kind`, and `mimetype`. These pieces of information can be accessed through class attributes of a given `File` object. For instance, let's revisit the test image we created above, and inspect its attributes.

```python
from pygsuite.drive import File


image = File(id="1TfNFLx9eHRIZoGupQ7S_n91kQjvXn5eM")

print(image.name)
print(image.kind)
print(image.mimetype)
```

When we run this code, we will see each piece of information printed as a string:

```
'Test Smiley'
'drive#file'
'image/png'
```

However, these do not represent the complete metadata available for a given file. The complete reference of all available properties is found [here on the Drive for Developers reference](https://developers.google.com/drive/api/v3/reference/files).

To access any of these properties, we can specify a list of fields we want returned to the file's `fetch_metadata` method. For instance, let's take a look a the file's creation time, and the time that we last viewed the file:

```python
from pygsuite.drive import File


image = File(id="1TfNFLx9eHRIZoGupQ7S_n91kQjvXn5eM")
print(image.fetch_metadata(fields=["createdTime", "viewedByMeTime"]))
```

This returns a dictionary with the key-value pairs of fields we requested, and their respective values.

```python
{'viewedByMeTime': '2021-11-15T14:50:09.350Z', 'createdTime': '2021-11-15T14:41:30.745Z'}
```

To retrieve _all_ the metadata fields available for a given file, we can use `"*"` to represent all fields in the request:

```python
from pygsuite.drive import File


image = File(id="1TfNFLx9eHRIZoGupQ7S_n91kQjvXn5eM")
all_fields = image.fetch_metadata(fields=["*"])
```

## Sharing files

Updating permissions is easily done using the `share` method for a given user, group, domain, or everyone:

```python
from pygsuite.drive import File
from pygsuite.enums import PermissionType


image = File(id="1TfNFLx9eHRIZoGupQ7S_n91kQjvXn5eM")
image.share(role=PermissionType.WRITER, user="test@gmail.com")
```

The `share` method takes inputs of the _type_, identifying the scope of the permission, and the _role_, identifying the operations that the _type_ can perform. Options for the _type_ include `user`, `group`, `domain`, `anyone` (represented by their corresponding parameters in the method), and options for the _role_ are represented by the `PermissionType` enumeration and include `PermissionType.OWNER`, `PermissionType.ORGANIZER`, `PermissionType.FILE_ORGANIZER`, `PermissionType.WRITER`, `PermissionType.COMMENTER`, `PermissionType.READER`. For more information on what operations a given role can perform, [see the documentation on roles here](https://developers.google.com/drive/api/v3/ref-roles).

A full email address should be provided for the `type` if sharing with a user or group, as in the example above: `user="test@gmail.com"`.

To share a file with anyone, simply set `anyone=True`.

## Downloading files

Coming soon!

## Deleting files

Coming soon!
