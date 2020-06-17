from pygsuite import ImageUploader, Document

BUCKET_NAME = "a_bucket"
# image uploader accepts either a string, dictionary, or filepath as the account_info
ACCOUNT_INFO = "/test/service_account.json"

im = ImageUploader(bucket=BUCKET_NAME, account_info=ACCOUNT_INFO)
public_url = im.signed_url_from_file(r"/test/image.png")
document = Document(id="Some_Document_ID")
document.body.add_image(public_url)
