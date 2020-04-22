from ast import literal_eval

import pytest

from pygsuite.docs.document import Document


@pytest.fixture
def test_document():
    with open("test_document.json") as file:
        return Document(_document=literal_eval(file.read()))
