from math import floor
from string import ascii_letters, ascii_uppercase

from pygsuite.common.style import Border
from pygsuite.sheets.cell import Cell


def index_to_alphabet(idx: int):
    out = ""
    count = floor(idx / 26)
    remainder = idx % 26
    if count:
        out = ascii_uppercase[count - 1]
    out += ascii_uppercase[remainder - 1]
    return out


def alphabet_to_index(cell_ref: str):
    idx = 0
    for char in cell_ref:
        if char in ascii_letters:
            idx = idx * 26 + (ord(char.upper()) - ord("A")) + 1
    return idx - 1


class Worksheet(object):
    """Worksheet object for the worksheets within a Spreadsheet
    """

    def __init__(self, worksheet, spreadsheet):
        """Method to initialize the class.

        Args:
            worksheet ():
            spreadsheet (pygsuite.sheets.Spreadsheet): the Google Spreadsheet object containing the Worksheet.
        """

        self._worksheet = worksheet
        self._spreadsheet = spreadsheet
        self._properties = self._worksheet["properties"]

    def __getitem__(self, cell_range):
        return self.values_from_range(cell_range).to_list()

    @property
    def name(self):
        return self._properties["title"]

    @property
    def id(self):
        return self._properties["sheetId"]

    @property
    def row_count(self):
        return self._properties["gridProperties"]["rowCount"]

    @property
    def column_count(self):
        return self._properties["gridProperties"]["columnCount"]

    def range_from_indexes(self, startcol: str, startrow: int, endcol: str, endrow: int):

        assert startcol <= endcol
        assert startrow <= endrow

        start_index = f"{index_to_alphabet(startcol)}{startrow}"
        end_index = f"{index_to_alphabet(endcol)}{endrow}"
        range_label = f"{self.name}!{start_index}:{end_index}"

        return range_label

    def values_from_range(self, cell_range: str):

        worksheet_range = f"{self.name}!{cell_range}"
        values = self._spreadsheet.get_values_from_range(worksheet_range).to_list()
        return values

    @property
    def values(self):

        worksheet_range = self.range_from_indexes(1, 1, self.column_count, self.row_count)
        values = self._spreadsheet.get_values_from_range(worksheet_range).to_list()
        return values

    @property
    def dataframe(self):

        worksheet_range = self.range_from_indexes(1, 1, self.column_count, self.row_count)
        df = self._spreadsheet.get_values_from_range(worksheet_range).to_df()
        return df

    def format_borders(
        self,
        start_row_index: int,
        end_row_index: int,
        start_column_index: int,
        end_column_index: int,
        borders: Border,
    ):

        request = {
            "updateBorders": {
                "range": {
                    "sheetId": self.id,
                    "startRowIndex": start_row_index,
                    "endRowIndex": end_row_index,
                    "startColumnIndex": start_column_index,
                    "endColumnIndex": end_column_index,
                }
            }
        }

        for border in borders:

            request["updateBorders"][border.position.value] = border.to_json()

        self._spreadsheet._spreadsheets_update_queue.append(request)

    def format_cells(
        self,
        start_row_index: int,
        end_row_index: int,
        start_column_index: int,
        end_column_index: int,
        cell: Cell,
    ):

        fields, cell_json = cell.to_json()

        request = {
            "repeatCell": {
                "range": {
                    "sheetId": self.id,
                    "startRowIndex": start_row_index,
                    "endRowIndex": end_row_index,
                    "startColumnIndex": start_column_index,
                    "endColumnIndex": end_column_index,
                },
                "cell": cell_json,
                "fields": fields,
            }
        }

        self._spreadsheet._spreadsheets_update_queue.append(request)
