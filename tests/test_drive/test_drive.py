import pytest

from pygsuite.drive import Drive


def test_drive__deprecation_warning(auth_test_clients):
    """Test for deprecation warning of older Drive functionality."""
    with pytest.deprecated_call():
        Drive()


def test_drive__find_files__deprecated(auth_test_clients, test_filled_folder):
    """"""
    from pygsuite.enums import MimeType

    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive()._find_files(type=MimeType.PLAIN_TEXT, name=child_text_file.name)
    assert child_text_file.id in [file.get("id") for file in files]


def test_drive__find_files(auth_test_clients, test_filled_folder):
    """"""
    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive().find_files(folder_id=filled_folder.id,)
    assert all(
        test_file.id in [file.id for file in files]
        for test_file in [child_text_file, child_sheets_file]
    )


def test_drive__find_files__by_name(auth_test_clients, test_filled_folder):
    """"""
    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive().find_files(
        folder_id=filled_folder.id,
        name=child_text_file.name,
    )
    assert child_text_file.id in [file.id for file in files]


def test_drive__find_files__by_type(auth_test_clients, test_filled_folder):
    """"""
    from pygsuite.enums import MimeType

    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive().find_files(
        folder_id=filled_folder.id,
        type=MimeType.SHEETS,
    )
    assert child_sheets_file.id in [file.id for file in files]


def test_drive__find_files__by_extra_conditions(auth_test_clients, test_filled_folder):
    """"""
    pass


def test_drive__find_files__support_all_drives(auth_test_clients, test_filled_folder):
    """"""
    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive().find_files(
        folder_id=filled_folder.id,
        support_all_drives=True,
    )

    assert all(
        test_file.id in [file.id for file in files]
        for test_file in [child_text_file, child_sheets_file]
    )


def test_drive__update_file_permissions(auth_test_clients):
    """"""
    pass


def test_drive__create_file(auth_test_clients):
    """"""
    pass


def test_drive__copy_file(auth_test_clients):
    """"""
    pass
