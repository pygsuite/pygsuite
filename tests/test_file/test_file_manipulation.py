import logging


def test_file_metadata__cached(test_text_file, caplog):
    caplog.set_level(logging.INFO)

    test_file = test_text_file
    mimetype = test_file.mimetype
    assert mimetype == "text/plain"

    mimetype = test_file.mimetype
    assert mimetype == "text/plain"
    assert "Using cached metadata..." in caplog.messages


def test_file_metadata__non_cached(test_text_file):
    test_file = test_text_file
    created_time = test_file.fetch_metadata(fields=["createdTime"]).get("createdTime")
    assert created_time is not None
