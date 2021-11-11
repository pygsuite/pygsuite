# from math import floor
from string import ascii_letters, ascii_uppercase

from pygsuite.constants import SHEETS_MAX_COLUMN_NUMBER


def index_to_alphabet(input_index: int) -> str:
    """Method to convert integer to A1 notation.

    :type input_index: int
    :param idx: Cell index to convert.

    :rtype: str
    :returns: A1 notation of the cell.
    """

    try:
        assert input_index <= SHEETS_MAX_COLUMN_NUMBER
    except AssertionError:
        raise ValueError(
            f"Input of column index {input_index} exceeds the maximum column number allowed of {SHEETS_MAX_COLUMN_NUMBER}."
        )

    a1_notation = ""

    while input_index > 0:
        input_index, remainder = divmod(input_index - 1, 26)
        a1_notation = ascii_uppercase[remainder] + a1_notation

    return a1_notation


def alphabet_to_index(cell_ref: str) -> int:
    """Method to convert A1 notation to an integer.
    NOTE: This method will return zero-centered indexes,
            despite `index_to_alphabet` taking one-centered index inputs.

    :type cell_ref: str
    :param cell_ref: A1 notation of cell to convert.

    :rtype: int
    :returns: Index notation of the cell.
    """

    idx = 0
    for char in cell_ref:
        if char in ascii_letters:
            idx = idx * 26 + (ord(char.upper()) - ord("A")) + 1

    return idx - 1
