import pandas as pd
from math import floor

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def index_to_alphabet(idx):
    out = ""
    count = floor(idx / 26)
    remainder = idx % 26
    if count:
        out = ALPHABET[count - 1]
    out += ALPHABET[remainder - 1]
    return out


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

    # @property
    # def values(self):
    #     return self._spreadsheet.values_get(self.name)

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

    # @property
    # def dataframe(self):
    #     values = self.all_values
    #     header = values[0]
    #     processed = []
    #     for row in values[1:]:
    #         if len(row) < len(header):
    #             diff = len(header) - len(row)
    #             row += [""] * diff
    #         processed.append(row)
    #     return pd.DataFrame.from_records(processed, columns=header)
