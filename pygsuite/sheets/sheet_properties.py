from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pygsuite.common.style import Color


class SheetType(Enum):
    """SheetType: The kind of sheet.

    Google Docs: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#SheetType
    """
    GRID = "GRID"
    OBJECT = "OBJECT"


@dataclass
class GridProperties:
    """GridProperties: Properties of a grid.

    Google Docs: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#GridProperties
    """

    row_count: Optional[int] = None
    column_count: Optional[int] = None
    frozen_row_count: Optional[int] = None
    frozen_column_count: Optional[int] = None
    hide_gridlines: Optional[bool] = None
    row_group_control_after: Optional[bool] = None
    colum_group_control_after: Optional[bool] = None

    def to_json(self):  # noqa: C901

        base = {}

        if self.row_count is not None:
            base["rowCount"] = self.row_count
        if self.column_count is not None:
            base["columnCount"] = self.column_count
        if self.frozen_row_count is not None:
            base["frozenRowCount"] = self.frozen_row_count
        if self.frozen_column_count is not None:
            base["frozenColumnCount"] = self.frozen_column_count
        if self.hide_gridlines is not None:
            base["hideGridlines"] = self.hide_gridlines
        if self.row_group_control_after is not None:
            base["rowGroupControlAfter"] = self.row_group_control_after
        if self.colum_group_control_after is not None:
            base["columnGroupControlAfter"] = self.colum_group_control_after

        return base


@dataclass
class SheetProperties:
    sheet_id: Optional[int] = None
    title: Optional[str] = None
    index: Optional[int] = None
    sheet_type: Optional[SheetType] = None
    grid_properties: Optional[GridProperties] = None
    hidden: Optional[bool] = None
    tab_color: Optional[Color] = None
    # TODO: tab_color_style
    right_to_left: Optional[bool] = None

    def __post_init__(self):

        # sheetId must be non-negative
        assert self.sheet_id >= 0

    def to_json(self):  # noqa: C901

        base = {}

        if self.sheet_id is not None:
            base["sheetId"] = self.sheet_id
        if self.title is not None:
            base["title"] = self.title
        if self.index is not None:
            base["index"] = self.index
        if self.sheet_type is not None:
            base["sheetType"] = self.sheet_type
        if self.grid_properties is not None:
            base["gridProperties"] = self.grid_properties.to_json()
        if self.hidden is not None:
            base["hidden"] = self.hidden
        if self.tab_color is not None:
            base["tabColor"] = self.tab_color.to_sheet_style()
        # TODO: if self.tab_color_style is not None:
        #     base["tabColorStyle"] = self.tab_color_style
        if self.right_to_left is not None:
            base["rightToLeft"] = self.right_to_left

        return base
