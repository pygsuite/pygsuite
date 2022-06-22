import pandas as pd

from pygsuite import PermissionType

BRIGHT_GREEN_HEX = "#72FF33"


def test_basic_instantiation(test_sheet):
    test_sheet.create_sheet(title="test_sheet", tab_color=BRIGHT_GREEN_HEX)
    test_sheet.flush()
    domain = "@gmail.com"
    test_sheet.share(user=f"pygsuite{domain}", role=PermissionType.WRITER)


def test_load_and_clear(test_sheet):
    new_sheet = test_sheet.create_and_return_sheet(title="test_upload", tab_color=BRIGHT_GREEN_HEX)
    test_data = [["1", "2", "3"], ["4", "5", "6"]]
    headers = ["cola", "colb", "colc"]
    insert = pd.DataFrame(data=test_data, columns=headers)
    new_sheet.insert_data_from_df(df=insert, insert_range="A1")
    new_sheet.flush()

    assert len(new_sheet.values) == 3

    assert new_sheet.values == [headers, *test_data]

    new_sheet.clear()

    assert len(new_sheet.values) == 0
