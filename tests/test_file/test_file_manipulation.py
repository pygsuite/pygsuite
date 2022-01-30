import logging


def test_file_metadata__cached(auth_test_clients, test_text_file, caplog):
    caplog.set_level(logging.INFO)

    test_file = test_text_file
    mimetype = test_file.mimetype
    assert mimetype == "text/plain"

    mimetype = test_file.mimetype
    assert mimetype == "text/plain"
    assert "Using cached metadata..." in caplog.messages


def test_file_metadata__non_cached(auth_test_clients, test_text_file):
    test_file = test_text_file
    created_time = test_file.fetch_metadata(fields=["createdTime"]).get("createdTime")
    assert created_time is not None


# TODO: add some comments and check content
# def test_file_comments(test_text_file):
#     test_file = test_text_file
#     comments = test_file.comments
#     assert comments == []


def test_file_sharing(auth_test_clients, test_text_file):
    from pygsuite.enums import PermissionType

    test_file = test_text_file
    shared = test_file.fetch_metadata(fields=["shared"]).get("shared")
    assert shared is False

    test_file.share(role=PermissionType.READER, user="sgaudet@wayfair.com")

    shared = test_file.fetch_metadata(ignore_cache=True, fields=["shared"]).get("shared")
    assert shared is True
