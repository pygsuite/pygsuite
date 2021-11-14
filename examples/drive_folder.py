from pygsuite import Clients
from pygsuite.drive.folder import Folder


# authenticate
Clients.local_file_auth("credentials.json")

folder = Folder(id="1WIR-FcfqujWs9fSPycjLSC9DOVCZT9DG")
print(folder.files)
