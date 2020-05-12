from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from pygsuite.common.style import BorderStyle, Color, TextStyle


@dataclass
class CellFormat:

    HORIZONTAL_ALIGNMENTS = ["LEFT", "CENTER", "RIGHT"]
    VERTICAL_ALIGNMENTS = ["TOP", "MIDDLE", "BOTTOM"]
    WRAP_STRATEGIES = ["OVERFLOW_CELL", "LEGACY_WRAP", "CLIP", "WRAP"]
    TEXT_DIRECTIONS = ["LEFT_TO_RIGHT", "RIGHT_TO_LEFT"]
    HYPERLINK_DISPLAY_TYPES = ["LINKED", "PLAIN_TEXT"]

    number_format: Optional[dict] = None
    background_color: Optional[Color] = None
    background_color_style: Optional[dict] = None
    borders: Optional[dict] = None
    padding: Optional[dict] = None
    horizontal_alignment: Optional[str] = None
    vertical_alignment: Optional[str] = None
    wrap_strategy: Optional[str] = None
    text_direction: Optional[str] = None
    text_format: Optional[TextStyle] = None
    hyperlink_display_type: Optional[str] = None
    text_rotation: Optional[dict] = None

    def to_json(self) -> Tuple[list, Dict]:  # noqa: C901

        base = {}
        fields_mask = []

        if self.number_format is not None:
            base["numberFormat"] = self.number_format

        if self.background_color is not None:
            base["backgroundColor"] = self.background_color

        if self.background_color_style is not None:
            base["backgroundColorStyle"] = self.background_color_style

        if self.borders is not None:
            base["borders"] = self.borders

        if self.padding is not None:
            base["padding"] = self.padding

        if self.horizontal_alignment is not None:
            assert self.horizontal_alignment in self.HORIZONTAL_ALIGNMENTS
            base["horizontalAlignment"] = self.horizontal_alignment

        if self.vertical_alignment is not None:
            assert self.vertical_alignment in self.VERTICAL_ALIGNMENTS
            base["verticalAlignment"] = self.vertical_alignment

        if self.wrap_strategy is not None:
            assert self.wrap_strategy in self.WRAP_STRATEGIES
            base["wrapStrategy"] = self.wrap_strategy

        if self.text_direction is not None:
            assert self.text_direction in self.TEXT_DIRECTIONS
            base["textDirection"] = self.text_direction

        if self.text_format is not None:
            masks, base["textFormat"] = self.text_format.to_sheet_style()
            fields_mask.extend(["textFormat." + field for field in masks])

        if self.hyperlink_display_type is not None:
            assert self.hyperlink_display_type in self.HYPERLINK_DISPLAY_TYPES
            base["hyperlinkDisplayType"] = self.hyperlink_display_type

        if self.text_rotation is not None:
            base["textRotation"] = self.text_rotation

        return fields_mask, base


@dataclass
class Cell:

    user_entered_value: Optional[dict] = None
    user_entered_format: Optional[CellFormat] = None
    hyperlink: Optional[str] = None
    note: Optional[str] = None
    text_format_runs: Optional[dict] = None
    data_validation: Optional[dict] = None
    pivot_table: Optional[dict] = None
    # TODO: should this object contain read-only objects?
    # effective_value: Optional[dict]  # READ ONLY
    # formatted_value: Optional[str]  # READ ONLY
    # effective_format: Optional[CellFormat]  # READ ONLY

    def to_json(self) -> Tuple[str, Dict]:  # noqa: C901

        base = {}
        fields_mask = []

        if self.user_entered_value is not None:
            base["userEnteredValue"] = self.user_entered_value
            fields_mask.append("userEnteredValue")

        if self.user_entered_format is not None:
            masks, base["userEnteredFormat"] = self.user_entered_format.to_json()
            fields_mask.extend(["userEnteredFormat." + field for field in masks])

        if self.hyperlink is not None:
            base["hyperlink"] = self.hyperlink
            fields_mask.append("hyperlink")

        if self.note is not None:
            base["note"] = self.note
            fields_mask.append("note")

        if self.text_format_runs is not None:
            base["textFormatRuns"] = self.text_format_runs
            fields_mask.append("textFormatRuns")

        if self.data_validation is not None:
            base["dataValidation"] = self.data_validation
            fields_mask.append("dataValidation")

        if self.pivot_table is not None:
            base["pivotTable"] = self.pivot_table
            fields_mask.append("pivotTable")

        return ",".join(fields_mask), base
