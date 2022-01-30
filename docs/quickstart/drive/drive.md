## Searching Files
Files can be searched for and retrieved 

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