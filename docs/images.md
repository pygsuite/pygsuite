# Images

Image insert may require a public URL.

In those cases, if you have a GCS bucket available, the recommended
work-around is signed URLs.

## Configuring the Bucket

### Step 1 - Cloud Storage

Follow the [package guide](https://pypi.org/project/google-cloud-storage/)
to get a project and bukcet configured.

It's recommended that you configure the bucket to have a short TTL
for your image uploads - there's no need to keep the images around.

It's also suggested to use a dedicated bucket.

### Create - Service Account

Create and download a service account credential file.

## Upload Client

The ImageUploader client can then be used
to upload a local file and automatically generate a signed URL
for it, which can then be passed into the standard upload methods.

```Python
{!../../docs_src/images/tutorial001.py!}
```

### Config Options

You can set the duration of the signed URls.

By default, this will be 15 minutes.
