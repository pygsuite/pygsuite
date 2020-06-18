Authorization to Google can be tricky.

All the API flows involve working with a Project - a namespaced section of GCP - 
that has the appropriate APIs enabled. The main APIs that pygsuite will require 
are the 

- Docs API
- Slides API
- Sheets API
- Drive API

The individual product APIs offer tailored interactions, while the drive API
is required for many management tasks. 

If you're using a personal account, you can start with any of Google's quickstarts
to enable the API you're interested in.

- [Docs](https://developers.google.com/docs/api/quickstart/python)
- [Sheets](https://developers.google.com/sheets/api/quickstart/python)
- [Slides](https://developers.google.com/slides/api/quickstart/python)

<!-- prettier-ignore-start -->
!!! tip
    If you're using a corporate account, you'll need to work with your Gsuite admins
    to get a project with the APIs enabled. 
<!-- prettier-ignore-end -->

### Getting Authentication

Any of the google tutorial flows will generate a 'credentials.json' file for you to save.

This token identifies an 'oauth identity' from your project, which you can 
then authorize to access your APIs. 

It's important to note that this identity itself does not grant access - what it is
used for is to generate an authentication flow, where you will consent to let the
item access to your APIs, and that will generate a token. This token is what then
grants access.

### Using a Local File

Once you've acquired a JSON file, you can authorize all your clients with the following code.

```python
from pygsuite import Clients

Clients.local_file_auth(r'path_to_your_key_file')

```

The first time this runs, you'll be prompted to go through the oauth flow.
After that, your generated credentials will be cached, and you can 
call the auth method pointing to your keyfile without having to go 
through the entire flow. 

### Using an Existing Credential Object

If you already have a valid credential object, you can also authorize with that directly.
This may be common if you're working through a job scheduler or sharing google suth
between multiple clients.

```python
from pygsuite import Clients

Clients.authorize(auth_object)

```

### Default Handling

Lastly, you can rely on Google's default credential handling if appropriate.

```python
from pygsuite import Clients

Clients.auth_default()

```

### After Handling

After you've authorized the Clients class, you're all set to use any of the APIs!
