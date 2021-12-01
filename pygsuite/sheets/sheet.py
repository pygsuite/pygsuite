from enum import Enum
from typing import Optional, Union, List, Dict

import pandas as pd
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from pygsuite import Clients
from pygsuite.common.drive_object import DriveObject
from pygsuite.common.parsing import parse_id
from pygsuite.enums import FileTypes
from pygsuite.sheets.sheet_properties import SheetProperties
from pygsuite.sheets.worksheet import Worksheet
from pygsuite.utility.decorators import retry


class ValueInputOption(Enum):
    """ValueInputOption: Determines how data should be interpreted.

    Google docs: https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
    """

    RAW = "RAW"
    USER_ENTERED = "USER_ENTERED"


class Dimension(Enum):
    """Dimension: Indicates which dimension an operation should apply to.

    Google docs: https://developers.google.com/sheets/api/reference/rest/v4/Dimension
    """

    ROWS = "ROWS"
    COLUMNS = "COLUMNS"


class ValueRenderOption(Enum):
    """ValueRenderOption: Determines how values should be rendered in the output.

    Google docs: https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption
    """

    FORMATTED_VALUE = "FORMATTED_VALUE"
    UNFORMATTED_VALUE = "UNFORMATTED_VALUE"
    FORMULA = "FORMULA"


class DateTimeRenderOption(Enum):
    """DateTimeRenderOption: Determines how dates should be rendered in the output.

    Google docs: https://developers.google.com/sheets/api/reference/rest/v4/DateTimeRenderOption
    """

    SERIAL_NUMBER = "SERIAL_NUMBER"
    FORMATTED_STRING = "FORMATTED_STRING"


def create_new_spreadsheet(title: str, client: Optional[Resource] = None):
    """Function to create a new spreadsheet given a client connection to the GSuite API,
       and a title for the new sheet.

    # TODO: add functionality to specify "filepath"?

    Args:
        service (googleapiclient.discovery.Resource): Connection to the Google API Sheets resource.
        title (str): Name for the new spreadsheet document

    Returns:
        id (str): the id of the spreadsheet
    """

    if not isinstance(title, str):
        raise TypeError("The name of the spreadsheet must be given as a string.")

    from pygsuite import Clients

    service = client or Clients.sheets_client

    request = {"properties": {"title": title}}

    spreadsheet = service.spreadsheets().create(body=request, fields="spreadsheetId").execute()
    id = spreadsheet.get("spreadsheetId")

    return Spreadsheet(client=service, id=id)


class ValueResponse(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_list(self):
        return list(self)

    def to_df(self, header: bool):
        """Method to use with self.get_values_from_range(self, cell_range) to return a pandas.DataFrame of values.

        Returns:
            df (pd.DataFrame): A pandas.DataFrame of the cell data gotten from get_values_from_range()
        """
        if header:
            header = self[0]
            records = self[1:]
            df = pd.DataFrame.from_records(data=records, columns=header)
        else:
            records = self
            df = pd.DataFrame.from_records(data=records)

        return df


class Spreadsheet(DriveObject):
    """Base class for the GSuite Spreadsheets API."""

    file_type = FileTypes.SHEETS

    def __init__(self, id: str, client: Optional[Resource] = None):
        """Method to initialize the class.

        The __init__ method accepts a client connection to the Google API, which it uses to retrieve the properties
        of the spreadsheet and create a _spreadsheet object to execute other requests of the API.

        Args:
            id (str): id of the Google Spreadsheet. Spreadsheet id can be found in the Spreadsheet URL between /d/ and /edit, eg:
                https://docs.google.com/spreadsheets/d/<spreadsheetId>/edit#gid=0
            client (googleapiclient.discovery.Resource): connection to the Google API Sheets resource.
        """

        self.service = client or Clients.sheets_client
        self.id = parse_id(id) if id else None
        DriveObject.__init__(self, id=id, client=client)

        self._spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.id).execute()
        self._properties = self._spreadsheet.get("properties")

        # queues to add to and run in flush()
        self._spreadsheets_update_queue: List[Dict] = []
        self._values_update_queue: List[Dict] = []

    @classmethod
    def create_new(cls, title: str, client=None):
        client = client or Clients.sheets_client
        body = {"properties": {"title": title}}
        new = client.spreadsheets().create(body=body).execute()
        return Spreadsheet(id=new.get("spreadsheetId"), client=client)

    def __getitem__(self, key: Union[str, int]):

        # if the key is an integer, use the int as worksheet index
        if isinstance(key, int):
            return self.worksheets[key]
        # if the key is a string, try to match to a worksheet name
        elif isinstance(key, str):
            try:
                return [worksheet for worksheet in self.worksheets if worksheet.name == key][0]
            except IndexError:
                raise KeyError(
                    "No worksheet with the title '{key}' exists. The worksheets included in your spreadsheet are: {worksheets}".format(
                        key=key, worksheets=[worksheet.name for worksheet in self.worksheets]
                    )
                )
        else:
            raise ValueError(
                "The key must be a string or integer. Use a string to get a worksheet by name, and integer to get a worksheet by index."
            )

    @property
    def worksheets(self):
        """List of Worksheet objects for each worksheet in the Spreadsheet."""
        return [Worksheet(sheet, self) for sheet in self._spreadsheet.get("sheets")]

    def refresh(self):
        """Method to refresh the spreadsheets API connection."""
        self._spreadsheet = self.service.spreadsheets().get(spreadsheetId=self.id).execute()

        self._spreadsheets_update_queue = []
        self._values_update_queue = []

    @retry((HttpError), tries=3, delay=10, backoff=5)
    def flush(
        self,
        reverse: bool = False,
        value_input_option: ValueInputOption = ValueInputOption.USER_ENTERED,
        include_values_in_response: bool = False,
        response_value_render_option: ValueRenderOption = ValueRenderOption.FORMATTED_VALUE,
        response_date_time_render_option: DateTimeRenderOption = DateTimeRenderOption.SERIAL_NUMBER,
    ):
        """Method to execute the change queues created through other methods.

        Args:
            reverse (bool): If True, the changes queued will be executed in reverse order.
            value_input_option (ValueInputOption): Indicates which dimension an operation should apply to.
            include_values_in_response (bool): If True, the API response will include the values changed.
            response_value_render_option (ValueRenderOption): Determines how values should be rendered in the output.
            response_date_time_render_option (DateTimeRenderOption): Determines how dates should be rendered in the output.

        Returns:
            response_dict (dict): Dictionary of API response JSON.
        """

        if reverse:
            _spreadsheets_update_queue = list(reversed(self._spreadsheets_update_queue))
            _values_update_queue = list(reversed(self._values_update_queue))
        else:
            _spreadsheets_update_queue = self._spreadsheets_update_queue
            _values_update_queue = self._values_update_queue

        response_dict = dict()

        if len(_spreadsheets_update_queue) > 0:
            response_dict["spreadsheets_update_response"] = (
                self.service.spreadsheets()
                .batchUpdate(body={"requests": _spreadsheets_update_queue}, spreadsheetId=self.id)
                .execute()
                .get("responses")
            )

        if len(_values_update_queue) > 0:
            response_dict["values_update_response"] = (
                self.service.spreadsheets()
                .values()
                .batchUpdate(
                    spreadsheetId=self.id,
                    body={
                        "valueInputOption": value_input_option.value,
                        "data": _values_update_queue,
                        "includeValuesInResponse": include_values_in_response,
                        "responseValueRenderOption": response_value_render_option.value,
                        "responseDateTimeRenderOption": response_date_time_render_option.value,
                    },
                )
                .execute()
                .get("responses")
            )

        # the queues are reset in the refresh() method
        # self._spreadsheets_update_queue = []
        # self._values_update_queue = []
        self.refresh()

        return response_dict

    def create_sheet(self, sheet_properties: Optional[SheetProperties] = None, **kwargs):
        """Add a new sheet to the spreadsheet."""
        sheet_properties = sheet_properties or SheetProperties(**kwargs)
        base = {"addSheet": {"properties": sheet_properties.to_json()}}
        self._spreadsheets_update_queue.append(base)
        return self

    def create_and_return_sheet(
        self, sheet_properties: Optional[SheetProperties] = None, **kwargs
    ) -> "Worksheet":
        before = [sheet.name for sheet in self.worksheets]
        self.create_sheet(sheet_properties=sheet_properties, **kwargs)
        self.flush()
        try:
            new = [sheet.name for sheet in self.worksheets if sheet.name not in before][0]
        except IndexError:
            raise ValueError("Error creating new sheet!")
        return self[new]

    def update_sheet(self, worksheet, sheet_properties):

        pass

    def clear_range(self, range: str):
        self.service.spreadsheets().values().clear(spreadsheetId=self.id, range=range).execute()
        return self

    def delete_sheet(self, title: Optional[str] = None, id: Optional[int] = None):
        """Method to delete a sheet by the title or id.

        Args:
            title (Optional: str): The title of a sheet to delete.
            id (Optional: int): The id of a sheet to delete.

        Returns:
            self (Spreadsheet): The object itself, to method chain.
        """

        # if an id is not given, title must be given; get id from title
        if not id:
            assert title is not None
            id = self.__getitem__(key=title).id

        base = {"deleteSheet": {"sheetId": id}}
        self._spreadsheets_update_queue.append(base)

        return self

    def get_values_from_range(self, cell_range: str) -> ValueResponse:
        """Method to get data from a Spreadsheet range. Returns a value object which can be chained
        to a dataframe or list.

        Args:
            cell_range (str): The range of cells for which to get data.

        Returns:
            self (Spreadsheet): The object itself, to method chain.
        """

        get_response = (
            self.service.spreadsheets()
            .values()
            .batchGet(spreadsheetId=self.id, ranges=[cell_range])
            .execute()
        )

        value_range = get_response.get("valueRanges")[0]  # TODO: cleanup
        values = value_range.get("values", [])
        return ValueResponse(values)

    def to_list(self, cell_range: str) -> list:
        """Method to use to return a list of values.

        Returns:
            self._values (list): A list of the cell data gotten from get_values_from_range()
        """
        return self.get_values_from_range(cell_range=cell_range)

    def to_df(self, cell_range: str, header: bool = True) -> pd.DataFrame:
        """Method to use to return a pandas.DataFrame of values.

        Returns:
            df (pd.DataFrame): A pandas.DataFrame of the cell data gotten from get_values_from_range()
        """
        return self.get_values_from_range(cell_range=cell_range).to_df(header=header)

    def insert_data(
        self, insert_range: str, values: list, major_dimension: Dimension = Dimension.ROWS
    ):
        """Method to insert data from a list into a given range in the Spreadsheet.

        Args:
            insert_range (str): The cell range in which to insert data.
            values (list): The data values, as a list, to insert.
            major_dimension (Dimension): Indicates which dimension an operation should apply to.

        Returns:
            self (Spreadsheet): The object itself, to method chain.
        """

        value_range = {
            "range": insert_range,
            "majorDimension": major_dimension.value,
            "values": values,
        }

        self._values_update_queue.append(value_range)

        return self

    def insert_data_from_df(
        self, df: pd.DataFrame, insert_range: str, major_dimension: Dimension = Dimension.ROWS
    ):
        """Method to insert data from a pd.DataFrame into a given range in the Spreadsheet.

        Args:
            df (pd.DataFrame): Dataframe of data to insert.
            insert_range (str): The cell range in which to insert data.
            major_dimension (Dimension): Indicates which dimension an operation should apply to.

        Returns:
            self (Spreadsheet): The object itself, to method chain.
        """

        # TODO: this insert_data_from_df method might be better as a method that we can
        # attach to insert_data--something like: mySpreadsheet.insert_data().from_df()

        header = df.columns.values.tolist()
        data = df.values.tolist()

        values = []
        if len(header) > 0:
            values.append(header)
        values.extend(data)

        self.insert_data(insert_range=insert_range, values=values, major_dimension=major_dimension)

        return self

    @property
    def url(self):
        return f"https://docs.google.com/spreadsheets/d/{self.id}"
