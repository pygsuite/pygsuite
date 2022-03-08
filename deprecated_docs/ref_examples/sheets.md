This guide assumes you have already created an auth object using the auth quickstart.

This example will walk you through an example using the sheets objects, which demonstrates some of the power to programmatically interact with Google Sheets.

This example will use data from the following resource:

- [Iris flower data set](https://en.wikipedia.org/wiki/Iris_flower_data_set) accessed through [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html)

## Get our spreadsheet

Humans work with names, not IDs. The `get_safe` method will fetch an existing presentation if it exists, or create it if it does not exist. Before doing this, we will import a few classes that will be useful down the road&mdash;we will cover each of these in more detail later.

```python
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

from pygsuite import Spreadsheet
from pygsuite.sheets.cell import Cell, CellFormat, HorizontalAlign
from pygsuite.sheets.sheet_properties import SheetProperties
from pygsuite.common.style import Color, TextStyle, Border, BorderStyle, BorderPosition
```

Let's get our spreadsheet object:

```python
title = "Iris Flower Data Set"
spreadsheet = Spreadsheet.get_safe(title)
```

## Adding Iris Data

First, let's import our practice Iris data set and try adding this to our spreadsheet. Using the `load_iris` function, we can load the Iris data and then convert it to a pandas DataFrame:

```python
iris = load_iris()
iris_df = pd.DataFrame(data=np.c_[iris["data"], iris["target"]], columns=iris["feature_names"] + ["target"])
```

Now that we have a dataframe, let's start off by adding the original dataset to a sheet in our spreadsheet so others can reference the original data. Here we can use the `anchor` parameter to insert our dataframe, starting with the upper-left cell in our anchor.

```python
spreadsheet["Sheet1"].insert_data_from_df(iris_df, anchor="A1")
spreadsheet.flush()
```

Let's quickly format the header row of the dataset in bold, to make it stand out from the data. We can define a `Cell` with a custom `CellFormat` and `TextStyle`.

```python
cell = Cell(user_entered_format=CellFormat(text_format=TextStyle(bold=True)))
spreadsheet["Sheet1"].format_cells(start_row_index=0, end_row_index=1, start_column_index=0, end_column_index=5, cell=cell)
spreadsheet.flush()
```

We can also add a border to separate the header from the row data.

```python
border = Border(position=BorderPosition.TOP, style=BorderStyle.SOLID_THICK, color=Color(red=0, green=0, blue=0))
spreadsheet["Sheet1"].format_borders(start_row_index=0, end_row_index=1, start_column_index=0, end_column_index=5, borders=[border])
spreadsheet.flush()
```

## Adding a New Slide with Formula Cells

Let's make a new worksheet in the spreadsheet that has a few descriptive metrics of the Iris data set. Using the `SheetProperties`, we can specify a title, id, position, and more for the new sheet. In this example, let's call this sheet "Summary" and make it the first tab in our spreadsheet.

```python
spreadsheet.create_sheet(SheetProperties(title="Summary", index=0))
spreadsheet.flush()
```

Now that we have made the new sheet, let's describe the data for the Sepals and Petals by:

- count
- average
- minimum
- maximum

All of these calculations have corresponding Google Sheets formulas that we can leverge to calculate these based on the data in our first sheet (Sheet1). First, let's start out by making a header row:

```python
header = ["Metric", "Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]
```

Next, let's map the metric names we want to use with the formula names we will wall. Given that all of these formulas accept a list of cells or cell range, we can iterate through the metrics.

```python
metrics = {"Count":"COUNT", "Average":"AVERAGE", "Min":"MIN", "Max":"MAX"}
```

All that's left is to create a loop to create a row for each metric that contains one formatted formula per column:

```python
calculations = []

for metric in metrics:

    row = [metric]

    for col in ["A", "B", "C", "D"]:

        formula = f"={calcs[calc]}(Sheet1!{col}2:{col}151)"
        row.append(formula)

    calculations.append(row)

values = [header]
values.extend(calculations)

spreadsheet["Summary"].insert_data(values=values, anchor="A1")
spreadsheet.flush()
```
