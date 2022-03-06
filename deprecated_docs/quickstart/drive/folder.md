# The Folder Object

The `Folder` object represents an important organizational tool in many GSuite operations. `Folder`s can be used to find files by name, type, author, and more.

## Creating a Folder

Creating a Google Drive folder is a common organizational task. Simply use the `Folder.create()` method to make a new folder:

```python
from pygsuite.drive import File


new_folder = Folder.create(
    name="My New Folder",
)

print(new_folder.id)
```

By default, the new folder will be created in the base of your Drive ("My Drive"). Instead, a folder can be created in a specific location by specifying the parent folder ID:

```python
from pygsuite.drive import File


new_nested_folder = Folder.create(
    name="My New Nested Folder",
    parent_folder_ids=["1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la"],
)

print(new_nested_folder.id)
```

## Listing Files in a Folder

Folders can be searched for their contents easily using the `Folder.get_files()` method. This method will query the folder's contents for files matching the given search by name, document type, and more.

In this simple example we will retrieve any Google Slides in our folder:

```python
from pygsuite.drive import Folder

folder = Folder(id="1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la")
files = folder.get_files()

for file in files:
    print(file)
```

### Searching with extra conditions

Using `pygsuite`'s included query objects allows you to construct additional search criteria. Constructing a query involves identifying a parameter to filter, the value you would like to use, and the operator to compare the two.

For instance, we could add a filter to only find starred files:

```python
from pygsuite.drive import Folder
from pygsuite.drive.query import Operator, QueryString, QueryTerm

query = QueryString(query_term=QueryTerm.STARRED, operator=Operator.EQUAL, True)

folder = Folder(id="1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la")
files = folder.get_files(extra_conditions=query)

for file in files:
    print(file)
```

Read more about the possible filters [here](), and more about constructing search queries in general [here]().

