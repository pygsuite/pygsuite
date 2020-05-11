from pygsuite import Clients
from analytics_utility_core.secrets import secret_store
from pygsuite import Clients
import googleapiclient

if __name__ == "__main__":
    auth = secret_store["bi-drive-automation"]

    Clients.authorize_string(auth)

    results = (
        Clients.drive_client.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])
    print(items)
    for item in items:
        file = Clients.drive_client_v2.files().get(fileId=item["id"]).execute()
        print(file)
        print(dir(file))
    # media_body = googleapiclient.http.MediaFileUpload(
    #     r'C:\Users\setup2.png',
    #     mimetype='media/png',
    #     resumable=True
    # )
    # # The body contains the metadata for the file.
    # body = {
    #     'title': 'test_pic',
    #     'description': 'a_test_pic',
    # }

    # Perform the request and print the result.
    # new_file = Clients.drive_client.files().create(
    #     body=body, media_body=media_body).execute()
    # print(new_file)
    # {'kind': 'drive#file', 'id': '1MedtBTFiT6hG8O9FSFKkrkKkpRCjLBH4', 'name': 'Untitled', 'mimeType': 'media/png'}
