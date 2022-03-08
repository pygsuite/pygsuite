from io import BytesIO
import requests

from pygsuite import Clients
from pygsuite.drive import File
from pygsuite.enums import GoogleDocFormat


# authenticate
Clients.local_file_auth("credentials.json")

# create an empty text file
text_file = File.create(
    name="Test Text Creation",
    mimetype="text/plain",
)

print(text_file.id)

# create an image object
response = requests.get(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1280px-SNice.svg.png"
)
bytes = BytesIO(response.content)

image_file = File.create(
    name="Test Smiley",
    mimetype="image/png",
    media_body=bytes,
)

print(image_file.id)

# upload an excel file and convert it to a Google Sheet
upload_file = r"examples\data\test data.xlsx"

sheets_file = File.upload(
    filepath=upload_file,
    name="Test Excel Upload",
    convert_to=GoogleDocFormat.SHEETS,
)

print(sheets_file.id)

# delete the test files
text_file.delete()
# image_file.delete()
sheets_file.delete()
