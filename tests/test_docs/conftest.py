import pytest
import json
from pygsuite.docs.document import Document
from ast import literal_eval


@pytest.fixture
def test_document():
    with open("test_document.json") as file:
        return Document(_document=literal_eval(file.read()))
