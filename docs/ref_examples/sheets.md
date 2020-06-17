This guide assumes you have already created an auth object using the auth quickstart.

## Create a new spreadsheet

The sheets integration allows the creation of a new spreadsheet. The created spreadsheet will be in the highest-level bucket of the account creating the spreadsheet&mdash;the Drive part of this package can be used to move the file into a desired bucket.

```python
from pygsuite.sheets.sheet import create_new_spreadsheet

title = "My first google sheet"
spreadsheet = create_new_spreadsheet(title=title)
```

When using this function, `client` is an optional parameter that can be used to provide an auth object.

## Interacting with a spreadsheet

To begin, create a spreadsheet object using the ID of the spreadsheet. From the [API docs](https://developers.google.com/sheets/api/guides/concepts): This ID is the value between the "/d/" and the "/edit" in the URL of your spreadsheet. For example, consider the following URL that references a Google Sheets spreadsheet:

```
https://docs.google.com/spreadsheets/d/spreadsheetId/edit#gid=0
```

The spreadsheet ID is a string containing letters, numbers, and some special characters. The following regular expression can be used to extract the spreadsheet ID from a Google Sheets URL:

```
/spreadsheets/d/([a-zA-Z0-9-_]+)
```

Once you have located the ID, create the spreadsheet object:

```python
from pygsuite.sheets.sheet import Spreadsheet

TEST_ID = "ABC123def456"
spreadsheet = Spreadsheet(id=TEST_ID)
```

The rest of the examples in this page will reference the `spreadsheet` object created here.

### Creating a worksheet

After creating a spreadsheet object, a worksheet can be created with the `create_sheet()` method. The method used to create the sheet uses an optional `SheetProperties` object that represents various details about the sheet to create, including options for the ID, title, index (position of the tab), tab color, and more. If not sheet properties are specified, defaults will be used by the Sheets API.

```python
spreadsheet.create_sheet()
```

Here is an example using specified sheet properties:

```python
from pygsuite.sheets.sheet_properties import SheetProperties

sheet_title = "NewSheet"
index = 0
sheet_properties = SheetProperties(title=sheet_title, index=index)
spreadsheet.create_sheet(sheet_properties=sheet_properties)
```

### Reading data from a spreadsheet

Data in a spreadsheet can be returned using the `get_values_from_range(cell_range)` method, where the `cell_range` is a range of cells to retrieve, in [A1 notation](https://developers.google.com/sheets/api/guides/concepts#a1_notation).

This method must be used in combination with either the `to_list()` or `to_df()` method to return data in a specific data structure.

```python
cell_range = "Sheet1!A1:B10"

values_list = spreadsheet.values_from_range(cell_range=cell_range).to_list()
values_df = spreadsheet.values_from_range(cell_range=cell_range).to_df()
```

### Inserting data into a spreadsheet

TODO

## Interacting with a worksheet

A given spreadsheet has one or multiple "worksheets" that represent that different tabs of data in the spreadsheet. Worksheet objects can be accessed in multiple ways from a spreadsheet object.

### Accessing a worksheet

Worksheet objects are accessible by using the integer index of the worksheet, where 0 represents the first worksheet in the spreadsheet, 1 represents the second, etc.

```python
worksheet = spreadsheet[0] # first tab in spreadsheet
```

Worksheet objects are also accessible by the sheet name:

```python
worksheet = spreadsheet["Sheet1"]
```

Lastly, worksheet objects are also accessible from a list of worksheets in the `worksheets` spreadsheet attribute. This last approach can also be used to get a list of worksheet objects for all the worksheets in a spreadsheet:

```python
worksheet = spreadsheet.worksheets[0]
worksheets_list = spreadsheet.worksheets
```

### Worksheet attributes

There are a number of pieces of information specific to a worksheet stored in the worksheet object. This includes:

**Worksheet name**

```
worksheet.name
```

**Worksheet ID**

```
worksheet.id
```

**Worksheet row count**

```
worksheet.row_count
```

**Worksheet column count**

```
worksheet.column_count
```

**Worksheet values**

All the data in a spreadsheet, in a list data structure.

```
worksheet.values
```

**Worksheet dataframe**

All the data in a spreadsheet, in a pandas DataFrame structure.

```
worksheet.dataframe
```

### Inserting data

TODO

### Reading data

Data in a worksheet can be returned using the `values_from_range(cell_range)` method, where the `cell_range` is a range of cells to retrieve, in [A1 notation](https://developers.google.com/sheets/api/guides/concepts#a1_notation).

This method to retrieve data returns a list of values:

```python
worksheet = spreadsheet["Sheet1"]
data = worksheet.values_from_range(cell_range="A1:B10")
```

### Formatting borders

TODO

### Formatting cells

TODO
