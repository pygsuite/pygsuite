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
from pygsuite.common.style import Color, TextStyle
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
iris_df = pd.DataFrame(data=np.c_[iris['data'], iris['target']], columns=iris['feature_names'] + ['target'])
```
