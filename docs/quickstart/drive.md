This quickstart assumes that you have already authorized your client, per the auth quickstart.

Authorization is the same for all examples.


### Listing Files
The drive client is useful for create, deleting, searching and modifying files. 

The pygsuite.drive module contans useful Enums, including the filetypes to search for
- Google Slides
- Google Docs
- Google Sheets

```python
from pygsuite import Drive
from pygsuite.drive import FileTypes

files = Drive().find_files(FileTypes.SLIDES)

for file in files:
    print(file)

```