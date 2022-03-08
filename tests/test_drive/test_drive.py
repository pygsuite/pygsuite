import pytest

from pygsuite.drive import Drive, File


def test_drive__deprecation_warning(auth_test_clients):
    """Test for deprecation warning of older Drive functionality."""
    with pytest.deprecated_call():
        Drive()


def test_drive__find_files__deprecated(auth_test_clients, test_filled_folder):
    """Test for soon-to-be deprecated _find_files functionality."""
    from pygsuite.enums import MimeType

    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive()._find_files(type=MimeType.PLAIN_TEXT, name=child_text_file.name)
    assert child_text_file.id in [file.get("id") for file in files]


def test_drive__find_files(auth_test_clients, test_filled_folder):
    """Test of basic find_files functionality."""
    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive().find_files(
        folder_id=filled_folder.id,
    )
    assert all(
        test_file.id in [file.id for file in files]
        for test_file in [child_text_file, child_sheets_file]
    )


def test_drive__find_files__by_name(auth_test_clients, test_filled_folder):
    """Test of find_files functionality, filtering by name."""
    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive().find_files(
        folder_id=filled_folder.id,
        name=child_text_file.name,
    )
    assert child_text_file.id in [file.id for file in files]


def test_drive__find_files__by_type(auth_test_clients, test_filled_folder):
    """Test of find_files functionality, filtering by MIME type."""
    from pygsuite.enums import MimeType

    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive().find_files(
        folder_id=filled_folder.id,
        type=MimeType.SHEETS,
    )
    assert child_sheets_file.id in [file.id for file in files]


def test_drive__find_files__by_extra_conditions(auth_test_clients, test_filled_folder):
    """Test of find_files functionality filtering by a user-specified query."""
    pass


def test_drive__find_files__support_all_drives(auth_test_clients, test_filled_folder):
    """Test of find_files functionality with support for all drives (wider search)."""
    filled_folder, child_text_file, child_sheets_file = test_filled_folder

    files = Drive().find_files(
        folder_id=filled_folder.id,
        support_all_drives=True,
    )
    assert all(
        test_file.id in [file.id for file in files]
        for test_file in [child_text_file, child_sheets_file]
    )


def test_drive__copy_file(auth_test_clients, test_text_file, test_folder):
    """Test of method to copy a file."""
    new_file = Drive().copy_file(
        file_id=test_text_file.id, title="test-copied-file", folder_id=test_folder.id
    )
    assert new_file.get("id") is not None
    new = File(id=new_file.get("id"))
    new.delete()
