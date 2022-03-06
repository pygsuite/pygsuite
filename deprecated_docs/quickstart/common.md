## Setup

This quickstart assumes that you have already authorized your client, per the auth quickstart.

Authorization is the same for all examples.

### Content
All drive files have common methods for common drive operations, such as sharing or moving.


### Sharing
```python
from pygsuite import Spreadsheet, PermissionType

sheet = Spreadsheet.get_safe('My test sheet')

sheet.share(user='test@gmail.com', role=PermissionType.WRITER)


```