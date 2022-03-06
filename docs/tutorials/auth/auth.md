# Authorization

Authorization is the first thing you will accomplish in getting started working with `pygsuite`, _and it can be tricky_! This tutorial will walk you through the basics of setting up authentication for your Google account, and using those credentials to authenticate in `pygsuite`.

## Understanding the basics

Before we begin setting up your authorization, it is helpful to understand a few core concepts. First, all of the workflows you may follow involve working with one or multiple applications from within the Google Suite, most commonly:

- [Google Drive](https://developers.google.com/drive/api/v3/quickstart/python)
- [Google Sheets](https://developers.google.com/sheets/api/quickstart/python)
- [Google Slides](https://developers.google.com/slides/api/quickstart/python)
- [Google Docs](https://developers.google.com/docs/api/quickstart/python)

If you are using a personal account, you can follow any of the links above and follow Google's guide to obtaining authentication credentials.

<!-- prettier-ignore-start -->
!!! tip
    If you're using a corporate account, you'll need to work with your GSuite admins
    to get a project with the APIs enabled. 
<!-- prettier-ignore-end -->

You may read more in Google's [documentation here](https://developers.google.com/identity/protocols/oauth2) on getting authentication credentials via their UI or API.

## Getting Authentication

Any of the Google quickstarts linked above will generate a JSON credential file for you to save.

This token identifies an 'oauth identity' from your project, which you can then authorize to access your APIs.

It's important to note that this identity itself does not grant access&mdash;instead, it is used to generate an authentication flow, where you will consent to let the item access your APIs, which in turn will generate a token. This token is what grants access.

### Using a local file

Once you've acquired a JSON file, you can authorize all your clients with the following code.

```python
from pygsuite import Clients

Clients.local_file_auth(r"path_to_your_key_file")
```

The first time this runs, you'll be prompted to go through the oauth flow.
After that, your generated credentials will be cached, and you can 
call the auth method pointing to your key file without having to go 
through the entire flow. 

### Using an Existing Credential Object

If you already have a valid [credential object](https://google-auth.readthedocs.io/en/latest/reference/google.auth.credentials.html#google.auth.credentials.Credentials),
you can also authorize with that directly.
This may be common if you're working through a job scheduler or sharing Google authentication
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
