from apiclient import errors
from apiclient.http import MediaFileUpload

# ...


def insert_file(service, title, description, parent_id, mime_type, filename):
    """Insert new file.

    Args:
      service: Drive API service instance.
      title: Title of the file to insert, including the extension.
      description: Description of the file to insert.
      parent_id: Parent folder's ID.
      mime_type: MIME type of the file to insert.
      filename: Filename of the file to insert.
    Returns:
      Inserted file metadata if successful, None otherwise.
    """
    media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
    body = {"title": title, "description": description, "mimeType": mime_type}
    # Set the parent folder.
    if parent_id:
        body["parents"] = [{"id": parent_id}]

    try:
        file = service.files().insert(body=body, media_body=media_body).execute()

        # Uncomment the following line to print the File ID
        # print 'File ID: %s' % file['id']

        return file
    except (errors.HttpError, Exception):
        print("An error occurred: %s" % Exception)
        return None
