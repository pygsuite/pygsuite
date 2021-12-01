import re
from typing import List, Optional, TYPE_CHECKING

import pandas as pd

from pygsuite.common.style import Border
from pygsuite.sheets.cell import Cell
from pygsuite.sheets.helpers import alphabet_to_index, index_to_alphabet

if TYPE_CHECKING:
    from pygsuite.sheets import Spreadsheet


# INDEX_SPLITTER = re.compile('(\d+)',s)


class Worksheet(object):
    """Worksheet object for the worksheets within a Spreadsheet"""

    def __init__(self, worksheet, spreadsheet: "Spreadsheet"):
        """Method to initialize the class.

        Args:
            worksheet ():
            spreadsheet (pygsuite.sheets.Spreadsheet): the Google Spreadsheet object containing the Worksheet.
        """

        self._worksheet = worksheet
        self._spreadsheet: "Spreadsheet" = spreadsheet
        self._properties = self._worksheet["properties"]

    def __getitem__(self, cell_range):
        return self.values_from_range(cell_range)

    def flush(self):
        self._spreadsheet.flush()
        return self

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

    def clear(self):
        """Method to clear all records in the sheet"""
        worksheet_range = self.range_from_indexes(1, 1, self.column_count, self.row_count)
        self._spreadsheet.clear_range(range=worksheet_range)
        return self

    def delete_sheet(self, flush: Optional[bool] = True):
        self._spreadsheet.delete_sheet(id=self.id)
        if flush:
            self._spreadsheet.flush()

    def range_from_indexes(self, startcol: int, startrow: int, endcol: int, endrow: int):

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
        borders: List[Border],
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

    def insert_data(
        self,
        values: list,
        insert_range: str = None,
        anchor: str = None,
        flush: bool = False,
        # major_dimension: Dimension = Dimension.ROWS
        # commented out because you'll need to move this to avoid circular imports
    ):
        # DO some input validation here
        anchor = insert_range.split(":")[0] if insert_range else anchor if anchor else "A1"

        split = re.split(r"(\d+)", anchor)
        x_raw = split[0]
        x = alphabet_to_index(x_raw)
        y = int(split[1])

        values_x = x + len(values[0])
        values_y = len(values) + y

        top_left = anchor
        bottom_right = index_to_alphabet(values_x) + str(values_y)

        # do some validation that it fits in rage if insert_rang was provided

        range = f"{self.name}!{top_left}:{bottom_right}"
        self._spreadsheet.insert_data(insert_range=range, values=values)

        if flush:
            self._spreadsheet.flush()

    def insert_data_from_df(
        self,
        df: pd.DataFrame,
        header: Optional[bool] = True,
        insert_range: Optional[str] = None,
        anchor: Optional[str] = None,
        flush: bool = False,
    ):

        values = []
        if header:
            values.append(df.columns.values.tolist())
        values.extend(df.values.tolist())

        self.insert_data(values=values, insert_range=insert_range, anchor=anchor, flush=flush)
