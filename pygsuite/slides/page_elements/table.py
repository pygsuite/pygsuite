from .base_element import BaseElement, Text


class TableCell(BaseElement):
    def __init__(self, element, presentation, table_id, row_index, column_index):
        BaseElement.__init__(self, element, presentation)
        self.table_id = table_id
        self.row_index = row_index
        self.column_index = column_index

    def __repr__(self):
        return f"cell {self.row_index} by {self.column_index} in table {self.table_id}"

    @property
    def text(self):
        if self._element.get("text"):
            return Text(self._element.get("text")).text
        return None

    @property
    def cell_location(self):
        return {"rowIndex": self.row_index, "columnIndex": self.column_index}

    def update_text(self, text, bullets=False, font_size=None, **kwargs):
        # only delete text if there is some
        if self.text:
            reqs = [
                {
                    "deleteText": {
                        "objectId": self.table_id,
                        "cellLocation": self.cell_location,
                        "textRange": {"type": "ALL"},
                    }
                }
            ]
        else:
            reqs = []
        reqs += [
            {
                "insertText": {
                    "objectId": self.table_id,
                    "cellLocation": self.cell_location,
                    "text": text,
                    "insertionIndex": 0,
                }
            }
        ]

        if bullets and text:
            reqs.append(
                {
                    "createParagraphBullets": {
                        "objectId": self.table_id,
                        "cellLocation": self.cell_location,
                        "textRange": {"type": "ALL"},
                    }
                }
            )

        if font_size and text:
            reqs.append(
                {
                    "updateTextStyle": {
                        "objectId": self.table_id,
                        "cellLocation": self.cell_location,
                        "style": {"fontSize": {"magnitude": font_size, "unit": "PT"}},
                        "textRange": {"type": "ALL"},
                        "fields": "fontSize",
                    }
                }
            )

        return self._presentation._mutation(reqs)

    def set_background_color(self, theme_color=None, rgb_color=None):
        assert theme_color or rgb_color
        assert not (theme_color and rgb_color)

        if theme_color:
            color = {"themeColor": theme_color}
        elif rgb_color:
            color = {
                "rgbColor": {
                    "red": rgb_color[0] / 256,
                    "green": rgb_color[1] / 256,
                    "blue": rgb_color[2] / 256,
                }
            }
        else:
            raise ValueError("No color provided")

        reqs = [
            {
                "updateTableCellProperties": {
                    "objectId": self.table_id,
                    "tableRange": {"location": self.cell_location, "rowSpan": 1, "columnSpan": 1},
                    "tableCellProperties": {
                        "tableCellBackgroundFill": {"solidFill": {"color": color, "alpha": 1}}
                    },
                    "fields": "tableCellBackgroundFill.solidFill.color",
                }
            }
        ]
        self._presentation._mutation(reqs)

    def set_border_color(self, theme_color=None, rgb_color=None, weight=2):
        assert theme_color or rgb_color
        assert not (theme_color and rgb_color)

        if theme_color:
            color = {"themeColor": theme_color}
        elif rgb_color:
            color = {
                "rgbColor": {
                    "red": rgb_color[0] / 256,
                    "green": rgb_color[1] / 256,
                    "blue": rgb_color[2] / 256,
                }
            }
        else:
            raise ValueError("No color provided")

        reqs = [
            {
                "updateTableBorderProperties": {
                    "objectId": self.table_id,
                    "tableRange": {"location": self.cell_location, "rowSpan": 1, "columnSpan": 1},
                    "tableBorderProperties": {
                        "tableBorderFill": {"solidFill": {"color": color, "alpha": 1}},
                        "weight": {"magnitude": weight, "unit": "PT"},
                    },
                    "fields": "tableBorderFill.solidFill.color,weight.magnitude",
                }
            }
        ]
        self._presentation._mutation(reqs)


class TableRow(BaseElement):
    def __init__(self, element, presentation, table_id, row_index):
        BaseElement.__init__(self, element, presentation)
        self.table_id = table_id
        self.row_index = row_index

    @property
    def cells(self):
        return [
            TableCell(
                val,
                self._presentation,
                table_id=self.table_id,
                column_index=idx,
                row_index=self.row_index,
            )
            for idx, val in enumerate(self._element["tableCells"])
        ]

    def __getitem__(self, item):
        return self.cells[item]


class Table(BaseElement):
    def __init__(self, element, presentation):
        BaseElement.__init__(self, element, presentation)
        self._details = self._element.get("table")

    def __getitem__(self, item):
        return self.rows[item]

    @property
    def size(self):
        return self.row_count * self.column_count

    @property
    def row_count(self):
        return self._details["rows"]

    @property
    def column_count(self):
        return self._details["columns"]

    @property
    def rows(self):
        return [
            TableRow(row, self._presentation, self.id, idx)
            for idx, row in enumerate(self._details["tableRows"])
        ]

    @property
    def id(self):
        return self._element["objectId"]

    @property
    def children(self):
        out = []
        for row in self.rows:
            for cell in row.cells:
                out.append(cell)
        return out
