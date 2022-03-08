from pygsuite import Clients, Drive


# authenticate
Clients.local_file_auth("credentials.json")

drive = Drive()

# simple search within folder
files = drive.find_files(
    folder_id="1WIR-FcfqujWs9fSPycjLSC9DOVCZT9DG",
)
print(files)

# restrict search to specific title
files = drive.find_files(
    folder_id="1WIR-FcfqujWs9fSPycjLSC9DOVCZT9DG",
    title="Test Sheet",
)
print(files)

# restrict search to specific type
from pygsuite.enums import GoogleMimeType

files = drive.find_files(
    folder_id="1WIR-FcfqujWs9fSPycjLSC9DOVCZT9DG",
    type=GoogleMimeType.DOCS,
)
print(files)


# search all drives--be careful wtih recursion!
files = drive.find_files(
    support_all_drives=True,
)
print(files)
