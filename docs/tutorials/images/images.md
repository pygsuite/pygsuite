# Images

Image inserts typically requires a public URL. 

This tutorial walks you through using Google Cloud's offerings - in this case, a Google Cloud Storage bucket - 
to host a public image and insert it.

You can replace GCS with any other public blob storage, such as an Amazon S3 bucket, or even a public
resource on github or google drive.

This guide in particular shows how to configure an uploader that can be integrated into pygsuite
to seamlessly generate secure public URLs from a local image. 

## Images with GCP

If you can work with GCP, you can get a public URL using signed URLs.

## Configuring the Bucket

### Step 1 - Cloud Storage

Follow the [package guide](https://pypi.org/project/google-cloud-storage/)
to get a project and bucket configured.

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
