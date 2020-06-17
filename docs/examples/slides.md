This guide assumes you have already created an auth object using the auth quickstart.

## Create a new slide deck



```python
from pygsuite.sheets.sheet import create_new_spreadsheet

title = "My first google sheet"
spreadsheet = create_new_spreadsheet(title=title)
```