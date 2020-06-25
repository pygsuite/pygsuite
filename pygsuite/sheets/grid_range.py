from dataclasses import dataclass
from math import floor
import re
from string import ascii_letters, ascii_uppercase
from typing import Optional


def index_to_a1(idx: int):
    out = ""
    count = floor(idx / 26)
    remainder = idx % 26
    if count:
        out = ascii_uppercase[count - 1]
    out += ascii_uppercase[remainder - 1]
    return out


def a1_to_index(a1: str):
    idx = 0
    for char in a1:
        if char in ascii_letters:
            idx = idx * 26 + (ord(char.upper()) - ord("A")) + 1
    return idx - 1


@dataclass
class GridRange:
    """A range on a sheet. All indexes are zero-based. Indexes are half open, e.g the start index is inclusive and the end index is exclusive
    [startIndex, endIndex). Missing indexes indicate the range is unbounded on that side.

    Google docs: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#GridRange
    """

    sheet_id: int
    start_row_index: Optional[int] = None
    end_row_index: Optional[int] = None
    start_column_index: Optional[int] = None
    end_column_index: Optional[int] = None

    @classmethod
    def from_string(cls, id: str, range_string: str) -> GridRange:
        """Method to create a GridRange object from an A1 notation string.

        Args:
            cls (GridRange): the class itself.
            id (str): the gid of the sheet.
            range_string (str): the cell range as a string in A1 notation.

        Returns:
            gridrange (GridRange): instantiated GridRange object.
        """

        # remove any dollar signs for frozen cell references
        range_string = range_string.replace("$", "")

        # see if the range_string contains a sheet name
        if "!" in range_string:
            sheet_name = range_string.split("!")[0]
            cell_range = range_string.split("!")[1]
        else:
            cell_range = range_string

        if ":" in cell_range:
            cell_range_start = cell_range.split(":")[0]
            cell_range_end = cell_range.split(":")[1]

            if re.match(r"/d+", cell_range_start) is not None:
                start_row_index = int(re.search(r"\d+", cell_range_start).group()) - 1
            if re.match(r"/d+", cell_range_end) is not None:
                end_row_index = int(re.search(r"\d+", cell_range_end).group()) - 1

            start_column_index = a1_to_index(cell_range_start)
            end_column_index = a1_to_index(cell_range_end)

        else:
            # cell range is a single column
            start_column_index = a1_to_index(cell_range)
            end_column_index = start_column_index + 1

        if start_row_index is not None and end_row_index is not None:
            grid_range = GridRange(
                sheet_id=id,
                start_row_index=start_row_index,
                end_row_index=end_row_index,
                start_column_index=start_column_index,
                end_column_index=end_column_index,
            )
        else:
            grid_range = GridRange(
                sheet_id=id,
                start_column_index=start_column_index,
                end_column_index=end_column_index,
            )

        return grid_range

    def to_json(self) -> dict:

        base = {"sheetId": self.sheet_id}

        if self.start_row_index is not None:
            base["startRowIndex"] = self.start_row_index
        if self.end_row_index is not None:
            base["endRowIndex"] = self.end_row_index
        if self.start_column_index is not None:
            base["startColumnIndex"] = self.start_column_index
        if self.end_column_index is not None:
            base["endColumnIndex"] = self.end_column_index

        return base

    def to_a1_string(self) -> str:

        pass
