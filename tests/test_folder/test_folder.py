import uuid

from pygsuite.drive import Folder


TEST_ID = uuid.uuid4()


def test_folder_creation(auth_test_clients):
    new_folder = Folder.create(name=f"Empty folder {TEST_ID}")
    assert new_folder.id is not None


def test_folder_creation__nested(auth_test_clients, test_folder):
    parent_folder_id = test_folder.id
    new_nested_folder = Folder.create(
        name=f"Empty nested folder {TEST_ID}",
        parent_folder_ids=[parent_folder_id]
    )
    assert new_nested_folder.id is not None
