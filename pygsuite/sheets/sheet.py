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
        raise TypeError("The name of the spreadsheet must be given as a string.")

    request = {"properties": {"title": title}}

    spreadsheet = service.spreadsheets().create(body=request, fields="spreadsheetId").execute()

    id = spreadsheet.get("spreadsheetId")

    return Spreadsheet(service=service, id=id)


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

    def __init__(
        self, id, client=None,
    ):
        """Method to initialize the class.

        The __init__ method accepts a client connection to the Google API, which it uses to retrieve the properties
        of the spreadsheet and create a _spreadsheet object to execute other requests of the API.

        Args:
            service (googleapiclient.discovery.Resource): connection to the Google API Sheets resource.
            id (str): id of the Google Spreadsheet. Spreadsheet id can be found in the Spreadsheet URL between /d/ and /edit, eg:
                https://docs.google.com/spreadsheets/d/<spreadsheetId>/edit#gid=0
        """

        from pygsuite import Clients

        self.service = client or Clients.sheets_client
        self.id = id

        self._spreadsheet = self.service.spreadsheets().get(spreadsheetId=id).execute()
        self._properties = self._spreadsheet.get("properties")

        # queues to add to and run in flush()
        self._spreadsheets_update_queue = []
        self._values_update_queue = []
        # self._values_get_queue = []

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
    def flush(
        self,
        reverse=False,
        value_input_option="RAW",
        include_values_in_response=False,
        response_value_render_option="FORMATTED_VALUE",
        response_date_time_render_option="SERIAL_NUMBER",
    ):

        assert value_input_option in self.VALUE_INPUT_OPTIONS
        assert response_value_render_option in self.VALUE_RENDER_OPTIONS
        assert response_date_time_render_option in self.DATE_TIME_RENDER_OPTIONS

        if reverse:
            _spreadsheets_update_queue = reversed(self._spreadsheets_update_queue)
            _values_update_queue = reversed(self._values_update_queue)
            # _values_get_queue = reversed(self._values_get_queue)
        else:
            _spreadsheets_update_queue = self._spreadsheets_update_queue
            _values_update_queue = self._values_update_queue
            # _values_get_queue = self._values_get_queue

        response_dict = dict()

        if len(_spreadsheets_update_queue) > 0:
            response_dict["spreadsheets_update_response"] = (
                self.service.spreadsheets()
                .batchUpdate(body={"requests": _spreadsheets_update_queue}, spreadsheetId=self.id)
                .execute()  # ["responses"]
            )

        if len(_values_update_queue) > 0:
            response_dict["values_update_response"] = (
                self.service.spreadsheets()
                .values()
                .batchUpdate(
                    spreadsheetId=self.id,
                    body={
                        "valueInputOption": value_input_option,
                        "data": _values_update_queue,
                        "includeValuesInResponse": include_values_in_response,
                        "responseValueRenderOption": response_value_render_option,
                        "responseDateTimeRenderOption": response_date_time_render_option,
                    },
                )
                .execute()  # ["responses"]
            )

        self._spreadsheets_update_queue = []
        self._values_update_queue = []
        # self._values_get_queue = []
        self.refresh()

        return response_dict

    def create_sheet(self):

        pass

    def get_values_from_ranges(
        self, ranges,
    ):

        get_response = (
            self.service.spreadsheets()
            .values()
            .batchGet(spreadsheetId=self.id, ranges=ranges)
            .execute()
        )

        # TODO: because the request supports getting data from multiple ranges at once, this is a list
        # however, the output of this is a litte bit messy at the moment--is a dict better or
        # limiting this to read one valueRange at a time?
        values_out = []

        for value_range in get_response.get("valueRanges"):

            values = value_range.get("values")
            values_out.append(values)

        return values_out

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

        for value_range in get_response.get("valueRanges"):

            # TODO: do we want to handle header rows here, or leave that to end users?
            # if headers are optional, would the option be for each range of data being fetched?

            values = value_range.get("values")
            df = pd.DataFrame.from_records(data=values)
            dfs[value_range.get("range")] = df

        return dfs

    def insert_data(
        self, insert_range, values, major_dimension="ROWS",
    ):

        assert major_dimension in self.DIMENSIONS

        value_range = {"range": insert_range, "majorDimension": major_dimension, "values": values}

        self._values_update_queue.append(value_range)

        return self

    def insert_data_from_df(
        self, df, insert_range, major_dimension="ROWS",
    ):

        # TODO: this insert_data_from_df method might be better as a method that we can
        # attach to insert_data--something like: mySpreadsheet.insert_data().from_df()

        header = df.columns.values.tolist()
        data = df.values.tolist()

        values = []
        if len(header) > 0:
            values.append(header)
        values.extend(data)

        self.insert_data(
            insert_range=insert_range, values=values, major_dimension=major_dimension,
        )
