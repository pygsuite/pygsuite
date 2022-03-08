import uuid

from pygsuite.drive import File, Folder


TEST_ID = uuid.uuid4()


def test_folder_creation(auth_test_clients):
    new_folder = Folder.create(name=f"Empty folder {TEST_ID}")
    assert new_folder.id is not None


def test_folder_creation__nested(auth_test_clients, test_folder):
    parent_folder_id = test_folder.id
    new_nested_folder = Folder.create(
        name=f"Empty nested folder {TEST_ID}", parent_folder_ids=[parent_folder_id]
    )
    assert new_nested_folder.id is not None
    new_nested_folder.delete()


def test_get_folder_files(auth_test_clients, test_folder):
    new_file_1 = File.create(
        name=f"Child file 1 {TEST_ID}", mimetype="text/plain", parent_folder_ids=[test_folder.id]
    )
    new_file_2 = File.create(
        name=f"Child file 2 {TEST_ID}", mimetype="text/plain", parent_folder_ids=[test_folder.id]
    )

    child_files = test_folder.get_files()
    assert all(file.id in [new_file_1.id, new_file_2.id] for file in child_files)

    new_file_1.delete()
    new_file_2.delete()
