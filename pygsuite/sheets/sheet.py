from googleapiclient.errors import HttpError
import pandas as pd

from pygsuite.sheets.worksheet import Worksheet
from pygsuite.utility.decorators import retry


def create_new_spreadsheet(service, title):
    """Function to create a new spreadsheet given a client connection to the GSuite API,
       and a title for the new sheet.

    # TODO: add functionality to specify "filepath"?

    Args:
        service (googleapiclient.discovery.Resource): connection to the Google API Sheets resource. 
        title (str): name for the new spreadsheet document

    Returns:
        id (str): the id of the spreadsheet
    """

    if not isinstance(title, str):
        raise TypeError(
            "The name of the spreadsheet must be given as a string.")

    request = {
        "properties": {
            "title": title
        }
    }

    spreadsheet = service.spreadsheets().create(
        body=request, fields="spreadsheetId").execute()

    id = spreadsheet.get("spreadsheetId")

    # TODO: do we want to return the Spreadsheet object instead? Or both?
    return id


class Spreadsheet:
    """Base class for the GSuite Spreadsheets API.
    """

    # ValueInputOption objects: https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
    VALUE_INPUT_OPTIONS = ["RAW", "USER_ENTERED"]
    # Dimensions objects: https://developers.google.com/sheets/api/reference/rest/v4/Dimension
    DIMENSIONS = ["ROWS", "COLUMNS"]
    # ValueRenderOption objects: https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption
    VALUE_RENDER_OPTIONS = ["FORMATTED_VALUE", "UNFORMATTED_VALUE", "FORMULA"]
    # DateTimeRenderOption objects: https://developers.google.com/sheets/api/reference/rest/v4/DateTimeRenderOption
    DATE_TIME_RENDER_OPTIONS = ["SERIAL_NUMBER", "FORMATTED_STRING"]

    def __init__(self, service, id):
        """Method to initialize the class.

        The __init__ method accepts a client connection to the Google API, which it uses to retrieve the properties
        of the spreadsheet and create a _spreadsheet object to execute other requests of the API.

        Args:
            service (googleapiclient.discovery.Resource): connection to the Google API Sheets resource.
            id (str): id of the Google Spreadsheet. Spreadsheet id can be found in the Spreadsheet URL between /d/ and /edit, eg:

                https://docs.google.com/spreadsheets/d/<spreadsheetId>/edit#gid=0
        """

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
                raise ValueError(
                    "No worksheet with the title '{key}' exists. The worksheets included in your spreadsheet are: {worksheets}".format(
                        key=key, worksheets=[worksheet.name for worksheet in self.worksheets]
                    )
                )
        else:
            raise ValueError("Please enter the sheet index or name you are trying to get.")

    @property
    def worksheets(self):
        return [Worksheet(sheet, self) for sheet in self._spreadsheet.get("sheets")]

    def refresh(self):
        self._spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.id).execute()

    @retry((HttpError), tries=3, delay=10, backoff=5)
    def flush(self, reverse=False):

        if reverse:
            base = reversed(self._spreadsheets_batchUpdate_queue)
        else:
            base = self._spreadsheets_batchUpdate_queue

        response_dict = dict()

        response_dict["spreadsheets_batchUpdate_response"] = (
            self.service.spreadsheets()
            .batchUpdate(body={"requests": base}, spreadsheetId=self.id)
            .execute()["responses"]
        )

        response_dict["values_batchUpdate_response"] = (
            self.service.spreadsheets()
            .values()
            .batchUpdate(spreadsheetId=self.id, body=self._values_batchUpdate_queue)
        )

        self._spreadsheets_batchUpdate_queue = []
        self._values_batchUpdate_queue = []
        self._values_batchGet_queue = []
        self.refresh()

        return response_dict

    def get_data_from_ranges(self, ranges):

        # TODO: should this method support getting multiple ranges of data at once?
        # The request allows for it, but this complicates the inputs / outputs of the method

        get_response = (
            self.service.spreadsheets()
            .values()
            .batchGet(spreadsheetId=self.id, ranges=ranges)
            .execute()
        )

        dfs = dict()

        for valueRange in get_response.get("valueRanges"):

            # TODO: do we want to handle header rows here, or leave that to end users?
            # if headers are optional, would the option be for each range of data being fetched?

            values = valueRange.get("values")
            df = pd.DataFrame.from_records(data=values)
            dfs[valueRange.get("range")] = df

        return dfs

    def insert_data_from_df(
        self,
        df,
        insert_range,
        # TODO: do we want these pythonic-ly named; something like value_input_option, major_dimension, etc.?
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

        # TODO: should header be optional parameter?
        # additionally, what about header row where header != column names of df?

        values = []
        if len(header) > 0:
            values.append(header)
        values.extend(data)

        valueRange = {"range": insert_range, "majorDimension": majorDimension, "values": values}

        request = {
            "valueInputOption": valueInputOption,
            "data": [valueRange],
            "includeValuesInResponse": False,
            "responseValueRenderOption": responseValueRenderOption,
            "responseDateTimeRenderOption": responseDateTimeRenderOption,
        }

        self._values_batchUpdate_queue.append(request)

        # response = (
        #     self.service.spreadsheets()
        #     .values()
        #     .batchUpdate(spreadsheetId=self.id, body=request)
        #     .execute()
        # )

        # return response
