# Sheets

`pygsuite` offers a number of methods to easily create and work with spreadsheets in Google.

## Creating spreadsheets

Get started by creating a new spreadsheet:

```python
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)
print(spreadsheet.url)
```

### Create spreadsheets in a specific location

As with creating any file type in `pygsuite`, you can specify the folder location
while creating the new object:

```python hl_lines="5"
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
    parent_folder_ids=["1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la"],
)
print(spreadsheet.url)
```

## Upload an Excel file as a new spreadsheet

You can also create a new spreadsheet from a local Excel file:

```python
from pygsuite import Spreadsheet

uploaded_sheet = Spreadsheet.upload(
    filepath="/path/to/file.xlsx",
    name="Uploaded Spreadsheet",
)
print(uploaded_sheet.url)
```

### Upload to a specific folder

Following the exact same pattern as spreadsheet creation, parent folder IDs can be specified
while uploading a spreadsheet.

```python hl_lines="6"
from pygsuite import Spreadsheet

uploaded_sheet = Spreadsheet.upload(
    filepath="/path/to/file.xlsx",
    name="Uploaded Spreadsheet",
    parent_folder_ids=["1EdtzquPnXhDNNo_gjUOJMl83Sm9BV3la"],
)
print(uploaded_sheet.url)
```

## Worksheets in a spreadsheet

Each spreadsheet contains a set of worksheets (the tabs of a Google Sheet).
You can access worksheets through the class attribute:

```python hl_lines="6"
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)
for worksheet in spreadsheet.worksheets:
    print(worksheet.name)
```

### Getting worksheets by index

You can access worksheets by their index (corresponding to their tab order in the spreadsheet):

```python hl_lines="6"
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)
first_worksheet = spreadsheet[0]
print(first_worksheet.name)
```

### Getting worksheets by name

Alternatively, you can access worksheets by their name:

```python hl_lines="6"
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)
first_worksheet = spreadsheet["Sheet1"]
print(first_worksheet.id)
```

### Creating a new worksheet

You can also add worksheets to your spreadsheet:

```python hl_lines="2 7 8 9 10"
from pygsuite import Spreadsheet
from pygsuite.sheets import SheetProperties

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)
spreadsheet.create_sheet(
    SheetProperties(name="A new sheet")
)
spreadsheet.flush()

new_worksheet = spreadsheet["A new sheet"]
```

The `SheetProperties` are used to specify properties of the new sheet to create.
Given that `pygsuite` is build on a pattern of batching API calls, running `create_sheet` on its own
does not call the API or fulfill the request to create a sheet. The `spreadsheet.flush()` is needed
to actually call the API and create the new sheet.

### Creating and returning a worksheet

You can create a new worksheet, including the call to Google's API to actually create the sheet:

```python hl_lines="7 8 9"
from pygsuite import Spreadsheet
from pygsuite.sheets import SheetProperties

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)
new_worksheet = spreadsheet.create_and_return_sheet(
    SheetProperties(name="A new sheet")
)
```

### Deleting worksheets

As easily as they can be created, worksheets can also be deleted:

```python hl_lines="12 13"
from pygsuite import Spreadsheet
from pygsuite.sheets import SheetProperties

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)
spreadsheet.create_sheet(
    SheetProperties(name="A new sheet")
)
spreadsheet.flush()

spreadsheet.delete_sheet("A new sheet")
spreadsheet.flush()
```

Once again, this method requires a subsequent "flush" to send the request to the Google Sheets API.

Alternatively, this can be called on a worksheet itself:

```python hl_lines="11 12"
from pygsuite import Spreadsheet
from pygsuite.sheets import SheetProperties

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)
new_worksheet = spreadsheet.create_and_return_sheet(
    SheetProperties(name="A new sheet")
)

new_worksheet.delete_sheet()
spreadsheet.flush()
```

Or even with an in-line `flush()`:

```python
new_worksheet.delete_sheet(flush=True)
```

## Writing data to a spreadsheet

Data can be inserted into a sheet in a number of ways.

### Insert data from a Panda's `DataFrame` object

Most often, you will likely be inserting data into a spreadsheet from a `DataFrame`:

```python hl_lines="10 11 12 13"
from pandas import DataFrame
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

spreadsheet.insert_data_from_df(
    df=df,
    insert_range="Sheet1!A1:B3",
).flush()
```

### Insert data from a list of values

Though it's less common for most users, you can insert data directly from a list as well:

```python hl_lines="14 15 16 17"
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

values = [
    ["A", "B", "C"],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
]

spreadsheet.insert_data(
    insert_range="Sheet1!A1:C4",
    values=values,
).flush()
```

### Inserting data within a worksheet

Similarly to the spreadsheet, you can insert data within a worksheet itself as well:

**From a DataFrame:**

```python hl_lines="10 11 12"
from pandas import DataFrame
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

spreadsheet["Sheet1"].insert_data_from_df(
    df=df,
)
spreadsheet.flush()
```

**From a list of values:**

```python hl_lines="14 15 16"
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

values = [
    ["A", "B", "C"],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
]

spreadsheet["Sheet1"].insert_data(
    values=values,
)
spreadsheet.flush()
```

The `insert_range` in these examples is automatically derived from the values/`DataFrame` by looking at the total number of columns and rows used (meaning it does not need to be specified).

<!-- prettier-ignore-start -->
!!! tip
    If specifying an `insert_range`, the worksheet's name is ommitted in the `insert_range`.
    Accessing the worksheet and inserting directly through it can alleviate needing to keep track
    of worksheet names, etc.
<!-- prettier-ignore-end -->

Similar to other worksheet methods, both of these insert methods also allow for in-line 'flushing.'

## Reading data from a spreadsheet

Just like writing data to a spreadsheet, reading data from a spreadsheet is just as easy.

### Get a Panda's `DataFrame` from a cell range in a spreadsheet

```python hl_lines="19 20 21"
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

values = [
    ["A", "B", "C"],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
]

spreadsheet.insert_data(
    insert_range="Sheet1!A1:C4",
    values=values,
).flush()

spreadsheet_data = spreadsheet.to_df(
    cell_range="Sheet1!A1:C4",
)
print(spreadsheet_data)
```

If your data does not contain a header row, set the parameter `header` to `False` to
circumvent the first row from being used as the column names in the output `DataFrame`.

### Get a list of values from a cell range in a spreadsheet

```python hl_lines="15 16 17"
from pandas import DataFrame
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

spreadsheet.insert_data_from_df(
    df=df,
    insert_range="Sheet1!A1:B3",
).flush()

spreadsheet_data = spreadsheet.to_list(
    cell_range="Sheet1!A1:B3",
)
print(spreadsheet_data)
```

### Reading data from within a worksheet

Just like writing data, reading is quick and simple from within a worksheet object:

**To a DataFrame:**

```python hl_lines="19 20"
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

values = [
    ["A", "B", "C"],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
]

spreadsheet["Sheet1"].insert_data(
    values=values,
)
spreadsheet.flush()

worksheet_df = spreadsheet["Sheet1"].dataframe
print(worksheet_df)
```

**To a list of values:**

```python hl_lines="15 16"
from pandas import DataFrame
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

spreadsheet["Sheet1"].insert_data_from_df(
    df=df,
)
spreadsheet.flush()

worksheet_values = spreadsheet["Sheet1"].values
print(worksheet_values)
```

Most notably when compared to working in a spreadsheet, the cell range is automatically determined
by the max column/row indexes. Therefore, the cell range does not need to be specified, but rather
is derived for you.

## Clearing data in a spreadsheet

Along with writing and reading data, you can clear data from a spreadsheet:

```python hl_lines="15"
from pandas import DataFrame
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

spreadsheet.insert_data_from_df(
    df=df,
    insert_range="Sheet1!A1:B3",
).flush()

spreadsheet.clear_range("Sheet1!A1:B3")
```

### Clearing data through a worksheet

You can also clear a cell range using a worksheet:

```python hl_lines="15"
from pandas import DataFrame
from pygsuite import Spreadsheet

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

spreadsheet.insert_data_from_df(
    df=df,
    insert_range="Sheet1!A1:B3",
).flush()

spreadsheet["Sheet1"].clear()
```

In this case, no cell range is given, and the entire worksheet is cleared.

## Format data in a spreadsheet

You can use the worksheet object to format cells and their borders.

### Format cells in a worksheet

Using a few objects (`TextStyle`, `CellFormat`, and `Cell`) you can define a given cell style,
and format a given cell range based on the row and column indexes:

```python hl_lines="2 3 16 17 18 19 20 21 22 23 24 25 26 27 28"
from pandas import DataFrame
from pygsuite import Spreadsheet, TextStyle
from pygsuite.sheets import Cell, CellFormat

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

spreadsheet["Sheet1"].insert_data_from_df(
    df=df,
    flush=True,
)

cell_format = CellFormat(
    text_format=TextStyle(bold=True)
)
bold = Cell(
    user_entered_format=cell_format
)
spreadsheet["Sheet1"].format_cells(
    start_row_index=0,
    end_row_index=1,
    start_column_index=0,
    end_column_index=2,
    cell=bold,
)
spreadsheet.flush()
```

### Format cell borders in a worksheet

Similar to formatting cells, you can format borders around those cells as well:

```python hl_lines="2 4 24 25 26 27 28 37 38 39 40 41 42 43"
from pandas import DataFrame
from pygsuite import Spreadsheet, TextStyle, Color
from pygsuite.sheets import Cell, CellFormat
from pygsuite.common.style import Border, BorderPosition, BorderStyle

spreadsheet = Spreadsheet.create(
    name="My First Spreadsheet",
)

df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

spreadsheet["Sheet1"].insert_data_from_df(
    df=df,
    flush=True,
)

cell_format = CellFormat(
    text_format=TextStyle(bold=True)
)
bold = Cell(
    user_entered_format=cell_format
)

bottom_border = Border(
    position=BorderPosition.BOTTOM,
    style=BorderStyle.SOLID,
    color=Color(hex="#000000"),
)

spreadsheet["Sheet1"].format_cells(
    start_row_index=0,
    end_row_index=1,
    start_column_index=0,
    end_column_index=2,
    cell=bold,
)
spreadsheet["Sheet1"].format_borders(
    start_row_index=0,
    end_row_index=1,
    start_column_index=0,
    end_column_index=2,
    borders=[bottom_border],
)
spreadsheet.flush()
```
