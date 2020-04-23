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
    # https://docs.google.com/uc?export=view&id=1MedtBTFiT6hG8O9FSFKkrkKkpRCjLBH4
    for item in items:
        permission = {"role": "reader", "type": "user", "emailAddress": "edickinson@wayfair.com"}
        output = (
            Clients.drive_client.permissions().create(fileId=item["id"], body=permission).execute()
        )
        print(output)
