from os.path import abspath, dirname, join

from pandas import DataFrame
from pandas.testing import assert_frame_equal

from pygsuite import Spreadsheet, TextStyle, Color
from pygsuite.common.style import Border, BorderPosition, BorderStyle
from pygsuite.sheets import Worksheet, SheetProperties, Cell, CellFormat


def test_spreadsheet__create_new(auth_test_clients):
    new_spreadsheet = Spreadsheet.create(
        name="New Empty Spreadsheet",
    )
    assert new_spreadsheet.id is not None
    new_spreadsheet.delete()


def test_spreadsheet__upload_excel(auth_test_clients):
    upload_file = join(dirname(dirname(abspath(__file__))), "test_sheets", "assets", "test data.xlsx")
    uploaded_sheet = Spreadsheet.upload(
        filepath=upload_file,
        name="Uploaded Spreadsheet",
    )
    assert uploaded_sheet.id is not None
    # just to assure us that we have created the right pygsuite object:
    assert uploaded_sheet.url.startswith("https://docs.google.com/spreadsheets/d/")
    uploaded_sheet.delete()


def test_spreadsheet__list_worksheets(auth_test_clients, test_sheet):
    assert len(test_sheet.worksheets) == 1
    assert isinstance(test_sheet[0], Worksheet)
    assert isinstance(test_sheet["Sheet1"], Worksheet)


def test_spreadsheet__add_worksheets(auth_test_clients, test_sheet):
    test_sheet.create_sheet(SheetProperties(title="Sheet2"))
    test_sheet.flush()
    assert len(test_sheet.worksheets) == 2

    sheet_3 = test_sheet.create_and_return_sheet(SheetProperties(title="Sheet3"))
    assert isinstance(sheet_3, Worksheet)
    assert len(test_sheet.worksheets) == 3


def test_spreadsheet__remove_worksheets(auth_test_clients, test_sheet):
    test_sheet.delete_sheet(title="Sheet2")
    test_sheet.flush()
    assert len(test_sheet.worksheets) == 2

    test_sheet["Sheet3"].delete_sheet(flush=True)
    assert len(test_sheet.worksheets) == 1


def test_spreadsheet__insert_data__from_df(auth_test_clients, test_sheet):
    df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

    response = test_sheet.insert_data_from_df(
        df=df,
        insert_range="Sheet1!A1:B3",
    ).flush()
    assert response.get("values_update_response")[0].get("updatedRange") == "Sheet1!A1:B3"


def test_spreadsheet__insert_data__from_list(auth_test_clients, test_sheet):
    test_sheet.create_sheet(SheetProperties(title="Sheet2"))

    values = [
        ["A", "B", "C"],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
    ]

    response = test_sheet.insert_data(
        insert_range="Sheet2!A1:C4",
        values=values,
    ).flush()
    assert response.get("values_update_response")[0].get("updatedRange") == "Sheet2!A1:C4"


def test_spreadsheet__format_cells(auth_test_clients, test_sheet):
    cell_format = CellFormat(
        text_format=TextStyle(bold=True)
    )
    bold = Cell(
        user_entered_format=cell_format
    )

    test_sheet["Sheet1"].format_cells(
        start_row_index=0,
        end_row_index=1,
        start_column_index=0,
        end_column_index=2,
        cell=bold,
    )
    response = test_sheet.flush()
    assert response is not None


def test_spreadsheet__format_borders(auth_test_clients, test_sheet):
    bottom_border = Border(
        position=BorderPosition.BOTTOM,
        style=BorderStyle.SOLID,
        color=Color(hex="#000000"),
    )

    test_sheet["Sheet1"].format_borders(
        start_row_index=0,
        end_row_index=1,
        start_column_index=0,
        end_column_index=2,
        borders=[bottom_border],
    )
    response = test_sheet.flush()
    assert response is not None


def test_spreadsheet__read_data_to_df(auth_test_clients, test_sheet):
    df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

    spreadsheet_data = test_sheet.to_df(
        cell_range="Sheet1!A1:B3",
    )
    # casting columns returned as 'object' to 'int64'
    spreadsheet_data = spreadsheet_data.astype("int64")

    assert assert_frame_equal(spreadsheet_data, df) is None


def test_spreadsheet__read_data_to_list(auth_test_clients, test_sheet):
    spreadsheet_data = test_sheet.to_list(
        cell_range="Sheet2!A1:C4",
    )

    values = [
        ["A", "B", "C"],
        ["1", "4", "7"],
        ["2", "5", "8"],
        ["3", "6", "9"],
    ]
    assert spreadsheet_data == values


def test_spreadsheet__clear_range(auth_test_clients, test_sheet):
    test_sheet.clear_range(range="Sheet1!A1:B3")
    test_sheet.clear_range(range="Sheet2!A1:C4")

    sheet_1 = test_sheet["Sheet1"].values
    sheet_2 = test_sheet["Sheet2"].values

    assert (len(sheet_1) == 0 and len(sheet_2) == 0)


def test_spreadsheet__insert_data__from_df__in_worksheet(auth_test_clients, test_sheet):
    df = DataFrame(data={"col1": [1, 2], "col2": [3, 4]})

    test_sheet["Sheet1"].insert_data_from_df(
        df=df,
        flush=True,
    )
    assert test_sheet["Sheet1"].values == [["col1", "col2"], ["1", "3"], ["2", "4"]]


def test_spreadsheet__insert_data__from_list__in_worksheet(auth_test_clients, test_sheet):
    values = [
        ["A", "B", "C"],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
    ]

    test_sheet["Sheet2"].insert_data(
        values=values,
        flush=True,
    )
    assert test_sheet["Sheet2"].values == [["A", "B", "C"], ["1", "4", "7"], ["2", "5", "8"], ["3", "6", "9"]]


def test_spreadsheet__clear_range__in_worksheet(auth_test_clients, test_sheet):
    test_sheet["Sheet1"].clear()
    test_sheet["Sheet2"].clear()

    sheet_1 = test_sheet["Sheet1"].values
    sheet_2 = test_sheet["Sheet2"].values

    assert (len(sheet_1) == 0 and len(sheet_2) == 0)
