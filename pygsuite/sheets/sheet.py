import pandas as pd

from pygsuite.sheets.worksheet import Worksheet
from pygsuite.utility.decorators import retry


class Spreadsheet:

    # ValueInputOption objects: https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
    VALUE_INPUT_OPTIONS = ["RAW", "USER_ENTERED"]
    # Dimensions objects: https://developers.google.com/sheets/api/reference/rest/v4/Dimension
    DIMENSIONS = ["ROWS", "COLUMNS"]

    def __init__(self, service, id):
        self.service = service
        self.id = id
        self._sheet = service.open_by_key(id)
        self._batchUpdate_queue = []

    def id(self):
        return self._sheet["id"]

    @retry((HttpError), tries=3, delay=10, backoff=5)
    def flush(self, reverse=False):

        if reverse:
            base = reversed(self._batchUpdate_queue)
        else:
            base = self._batchUpdate_queue

        update_response = (
            self.service.spreadsheets()
            .batchUpdate(body={"requests": base}, spreadsheetId=self.id)
            .execute()["replies"]
        )
        self._batchUpdate_queue = []
        self.refresh()
        return update_response

    @property
    def worksheets(self):
        return [Worksheet(item, self._sheet) for item in self._sheet.worksheets()]

    def __getitem__(self, item):
        return self.worksheets[item]

    def refresh(self):
        self._sheet = self.service.open_by_key(self.id)

    def get_data_from_ranges(self, ranges):

        get_response = self._client.spreadsheets().values().batchGet(
            spreadsheetId=self.id, ranges=ranges).execute()

        dfs = dict()

        for valueRange in get_response.get("valueRanges"):

            values = valueRange.get("values")
            df = pd.DataFrame.from_records(data=values)
            dfs[valueRange.get("range")] = df

        return dfs

    def insert_data_from_df(self, df, range, valueInputOption="RAW", majorDimension="ROWS"):

        # TODO: change to helpful exceptions
        assert valueInputOption in self.VALUE_INPUT_OPTIONS
        assert majorDimension in self.DIMENSIONS

        data = df.values.tolist()

        valueRange = {
            "range": range,
            "majorDimension": majorDimension,
            "values": data
        }

        request = {
            "valueInputOption": valueInputOption,
            "data": [valueRange]
        }

        self._batchUpdate_queue.append(request)

    def
