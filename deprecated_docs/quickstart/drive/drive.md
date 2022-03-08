_This quickstart assumes that you have already authorized your client, per the [auth quickstart](./auth.md). Authorization is the same for all examples._

# The Drive object

The `Drive` object holds core functionality for finding and organizing files in Google Drive.

## Searching Files

<!-- prettier-ignore -->
!!! warning
    **Deprecation warning**: this functionality is replaced by the `Folder.get_files()` method, which is preferred as it is often more efficient than searching an entire Drive. In the future, this function may be moved or removed.
<!-- prettier-ignore-end -->

Files can be searched for and retrieved using the `Drive.find_files()` method. This method will query the user's Drive (and any shared Drives if chosen) for files matching the given search by name, document type, and more.

In this simple example we will retrieve any Google Slides in our personal Drive:

```python
from pygsuite.drive import Drive, GoogleMimeType

files = Drive().find_files(type=GoogleMimeType.SLIDES)

for file in files:
    print(file)
```

<!-- prettier-ignore -->
!!! tip
    To use legacy functionality, please use the `Drive._find_files()` method&mdash;however, this method will likely be removed in future releases.
<!-- prettier-ignore-end -->

### Searching for a specific name

To improve our search, we can include the name of the file we are searching for:

```python
from pygsuite.drive import Drive, GoogleMimeType

files = Drive().find_files(
    type=GoogleMimeType.SLIDES,
    name="Important Presentation for Boss",
)

for file in files:
    print(file)
```

By default, the parameter `exact_match` will be set to `True`, meaning that only files with names matching exactly will be returned. However, this can be set to `False`, in which case any file with a name that contains the string given for the `name` will be included. For instance, we could broaden our search:

```python
from pygsuite.drive import Drive, GoogleMimeType

files = Drive().find_files(
    type=GoogleMimeType.SLIDES,
    name="Important Presentation",
    exact_match=False,
)

for file in files:
    print(file)
```

### Searching outside of your Drive

Use the parameter `support_all_drives` to include files in shared drives as well as My Drive in the search results:

```python
from pygsuite.drive import Drive, GoogleMimeType

files = Drive().find_files(
    type=GoogleMimeType.SLIDES,
    name="Important Presentation for Boss",
    support_all_drives=True,
)

for file in files:
    print(file)
```

### Searching with extra conditions

Using `pygsuite`'s included query objects allows you to construct additional search criteria. Constructing a query involves identifying a parameter to filter, the value you would like to use, and the operator to compare the two.

For instance, we could add a filter to only find starred files:

```python
from pygsuite.drive import Drive, GoogleMimeType
from pygsuite.drive.query import Operator, QueryString, QueryTerm

query = QueryString(query_term=QueryTerm.STARRED, operator=Operator.EQUAL, True)

files = Drive().find_files(
    type=GoogleMimeType.SLIDES,
    name="Important Presentation for Boss",
    extra_conditions=query,
)

for file in files:
    print(file)
```

Read more about the possible filters [here](), and more about constructing search queries in general [here]().
