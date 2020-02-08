import pandas as pd
from math import floor
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def index_to_alphabet(idx):
    out = ''
    count = floor(idx/26)
    remainder = idx%26
    if count:
        out = ALPHABET[count-1]
    out += ALPHABET[remainder-1]
    return out



class Worksheet(object):
    def __init__(self, element, sheet):
        self._worksheet = element
        self._sheet = sheet
        self._properties = self._worksheet._properties

    @property
    def name(self):
        return self._properties['title']

    @property
    def row_count(self):
        return self._properties['gridProperties']['rowCount']

    @property
    def column_count(self):
        return self._properties['gridProperties']['columnCount']

    @property
    def values(self):
        return self._sheet.values_get(self.name)
        # out = []
        # for idx in range(1,self.row_count):
        #     out.append(self._worksheet.row_values(idx))
        # return out

    def values_range(self, startcol, startrow, endcol, endrow):
        assert startcol<=endcol
        assert startrow<=endrow
        start_index = f'{index_to_alphabet(startcol)}{startrow}'
        end_index = f'{index_to_alphabet(endcol)}{endrow}'
        range_label = f'{self.name}!{start_index}:{end_index}'
        return self._sheet.values_get(range_label)

    @property
    def all_values(self):
        output = self.values_range(1, 1, self.column_count, self.row_count)
        return output['values']



    @property
    def dataframe(self):
        values = self.all_values
        header = values[0]
        processed = []
        for row in values[1:]:
            if len(row)<len(header):
                diff = len(header)-len(row)
                row += ['']*diff
            processed.append(row)
        return pd.DataFrame.from_records(processed, columns = header)
