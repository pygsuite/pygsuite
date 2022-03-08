# Folders

**pygsuite** makes it simple to search and organize content in Google Drive folders.

## Creating folders

Create a new folder with a given name:

```python
from pygsuite import Folder

new_folder = Folder.create(name="My Folder")
print(new_folder.url)
```

### Creating a folder within a folder (_inception_)

Folders can be nested simply by adding the parent folder's ID:

```python hl_lines="5"
from pygsuite import Folder

new_folder = Folder.create(
    name="My Nested Folder",
    parent_folder_ids=["1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la],
)
print(new_folder.url)
```

## Listing files in a folder

You can return a list of the files in a folder easily, making for nice iteration over documents within a given folder:

```python
from pygsuite import Folder

folder = Folder(id="1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la")
files = folder.get_files()

for file in files:
    print(file.url)
```
