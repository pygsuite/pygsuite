from math import floor
from string import ascii_letters, ascii_uppercase
from typing import Union

from pygsuite.common.style import BorderStyle
from pygsuite.sheets.cell import Cell


def index_to_alphabet(idx):
    out = ""
    count = floor(idx / 26)
    remainder = idx % 26
    if count:
        out = ascii_uppercase[count - 1]
    out += ascii_uppercase[remainder - 1]
    return out


def alphabet_to_index(cell_ref):
    idx = 0
    for char in cell_ref:
        if char in ascii_letters:
            idx = idx * 26 + (ord(char.upper()) - ord("A")) + 1
    return idx - 1


class Worksheet(object):
    def __init__(self, worksheet, spreadsheet):
        self._worksheet = worksheet
        self._spreadsheet = spreadsheet
        self._properties = self._worksheet["properties"]

    def __getitem__(self, cell_range):
        return self.values_from_range(cell_range)

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

    def range_from_indexes(self, startcol, startrow, endcol, endrow):

        assert startcol <= endcol
        assert startrow <= endrow

        start_index = f"{index_to_alphabet(startcol)}{startrow}"
        end_index = f"{index_to_alphabet(endcol)}{endrow}"
        range_label = f"{self.name}!{start_index}:{end_index}"

        return range_label

    def values_from_range(self, cell_range):

        worksheet_range = f"{self.name}!{cell_range}"
        df_dict = self._spreadsheet.get_data_from_ranges(worksheet_range)
        return df_dict[worksheet_range]

    @property
    def all_values(self):

        worksheet_range = self.range_from_indexes(1, 1, self.column_count, self.row_count)
        values = self._spreadsheet.get_data_from_ranges(worksheet_range)
        return values

    def format_borders(
        self, start_row_index, end_row_index, start_column_index, end_column_index, border_styles,
    ):

        assert isinstance(border_styles, Union[list, BorderStyle])

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

        for border_style in border_styles:

            request["updateBorders"][border_style.position] = border_style.to_json()

        self._spreadsheet._spreadsheets_update_queue.append(request)

    def format_cells(
        self, start_row_index, end_row_index, start_column_index, end_column_index, cell,
    ):

        assert isinstance(cell, Cell)

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
