from ast import literal_eval

import pytest

from pygsuite.docs.document import Document
import os

script_dir = os.path.dirname(__file__)


@pytest.fixture
def static_test_document():
    with open(os.path.join(script_dir, "test_document.json_capture")) as file:
        return Document(_document=literal_eval(file.read()), local=True)
