from googleapiclient.errors import HttpError
import pandas as pd

from pygsuite.sheets.worksheet import Worksheet
from pygsuite.utility.decorators import retry


class Spreadsheet:

    # ValueInputOption objects: https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
    VALUE_INPUT_OPTIONS = ["RAW", "USER_ENTERED"]
    # Dimensions objects: https://developers.google.com/sheets/api/reference/rest/v4/Dimension
    DIMENSIONS = ["ROWS", "COLUMNS"]
    # ValueRenderOption objects: https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption
    VALUE_RENDER_OPTIONS = ["FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"]
    # DateTimeRenderOption objects: https://developers.google.com/sheets/api/reference/rest/v4/DateTimeRenderOption
    DATE_TIME_RENDER_OPTIONS = ["SERIAL_NUMBER", "FORMATTED_STRING"]

    def __init__(self, service, id):
        self.service = service
        self.id = id
        self._spreadsheet = self.service.spreadsheets().get(spreadsheetId=id).execute()
        self._properties = self._spreadsheet.get("properties")

        # queues to add to and run in flush()
        self._spreadsheets_batchUpdate_queue = []
        self._values_batchUpdate_queue = []
        self._values_batchGet_queue = []

    def __getitem__(self, key):

        # if the key is an integer, use the int as worksheet index
        if isinstance(key, int):
            return self.worksheets[key]
        # if the key is a string, try to match to a worksheet name
        elif isinstance(key, str):
            try:
                return [worksheet for worksheet in self.worksheets if worksheet.name == key][0]
            except ValueError:
                raise ValueError("No worksheet with the title '{key}' exists. The worksheets included in your spreadsheet are: {worksheets}".format(key=key, worksheets=[worksheet.name for worksheet in self.worksheets]))
        else:
            raise ValueError("Please enter the sheet index or name you are trying to get.")

    @property
    def worksheets(self):
        return [Worksheet(sheet, self) for sheet in self._spreadsheet.get("sheets")]

    @retry((HttpError), tries=3, delay=10, backoff=5)
    def flush(self, reverse=False):

        if reverse:
            base = reversed(self._spreadsheets_batchUpdate_queue)
        else:
            base = self._spreadsheets_batchUpdate_queue

        update_response = (
            self.service
            .spreadsheets()
            .batchUpdate(body={"requests": base}, spreadsheetId=self.id)
            .execute()["responses"]
        )

        self._spreadsheets_batchUpdate_queue = []
        self._values_batchUpdate_queue = []
        self._values_batchGet_queue = []
        self.refresh()
        return update_response

    def refresh(self):
        self._spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.id).execute()

    def get_data_from_ranges(self, ranges):

        get_response = (
            self.service.spreadsheets()
            .values()
            .batchGet(spreadsheetId=self.id, ranges=ranges)
            .execute()
        )

        dfs = dict()

        for valueRange in get_response.get("valueRanges"):

            # TODO: do we want to handle header rows here, or leave that to end users?

            values = valueRange.get("values")
            df = pd.DataFrame.from_records(data=values)
            dfs[valueRange.get("range")] = df

        return dfs

    def insert_data_from_df(
        self,
        df,
        range,
        valueInputOption="RAW",
        majorDimension="ROWS",
        responseValueRenderOption="FORMATTED_VALUE",
        responseDateTimeRenderOption="SERIAL_NUMBER",
    ):

        # TODO: change to helpful exceptions

        assert valueInputOption in self.VALUE_INPUT_OPTIONS
        assert majorDimension in self.DIMENSIONS
        assert responseValueRenderOption in self.VALUE_RENDER_OPTIONS
        assert responseDateTimeRenderOption in self.DATE_TIME_RENDER_OPTIONS

        header = df.columns.values.tolist()
        data = df.values.tolist()

        values = []
        if len(header) > 0:
            values.append(header)
        for row in data:
            values.append(row)

        valueRange = {"range": range, "majorDimension": majorDimension, "values": values}

        request = {
            "valueInputOption": valueInputOption,
            "data": [valueRange],
            "includeValuesInResponse": False,
            "responseValueRenderOption": responseValueRenderOption,
            "responseDateTimeRenderOption": responseDateTimeRenderOption,
        }

        response = (
            self.service.spreadsheets()
            .values()
            .batchUpdate(spreadsheetId=self.id, body=request)
            .execute()
        )

        return response
