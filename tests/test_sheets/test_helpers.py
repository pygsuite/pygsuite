from pygsuite.constants import SHEETS_MAX_COLUMN_NUMBER
from pygsuite.sheets.helpers import index_to_alphabet, alphabet_to_index


def test_index_to_alphabet():

    assert index_to_alphabet(1) == "A"
    assert index_to_alphabet(SHEETS_MAX_COLUMN_NUMBER) == "ZZZ"
    assert index_to_alphabet(89) == "CK"


def test_alphabet_to_index():

    assert alphabet_to_index("A") == 0
    assert alphabet_to_index("ZZZ") == SHEETS_MAX_COLUMN_NUMBER - 1
    assert alphabet_to_index("CK") == 88
