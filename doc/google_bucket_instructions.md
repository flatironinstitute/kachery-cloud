# Configuring Google bucket for use with kachery-cloud

Guide outline

* Create an account and sign in to the [Google Cloud Console](https://console.cloud.google.com/)
* Create a new Google Cloud Project (you could call it kachery-zone-test1)
* Create a new bucket
    - Navigate to Cloud Storage within your project
    - Create Bucket
    - The bucket name is globally unique
    - Choose a region: Pay attention to the region you choose (I don't think you can modify that later)
    - Standard storage class
    - The bucket is going to be public for the kachery file bucket, but private for the admin bucket
    - Use Uniform access control
    - Otherwise, you can use the default options
* For the public bucket, allow public reading of objects
    - Navigate to the bucket Permissions tab
    - Grant Access
    - Principals: allUsers
    - Role: Storage Object Viewer
    - Save
* For the public bucket, set up Cross-origin resource sharing (CORS)
    - Unfortunately this cannot be set in the web console
    - You will need to use gsutil from your computer instead
    - [Install and configure gsutil](https://cloud.google.com/storage/docs/gsutil_install)
    - Set the CORS configuration: https://cloud.google.com/storage/docs/configuring-cors#gsutil
    - See the example CORS configuration below (which you can paste into a `cors.json`)
    - `gsutil cors set cors.json gs://BUCKET_NAME` (replace BUCKET_NAME)
* Create a service account for kachery access
    - Navigate to IAM -> Service Accounts
    - Create a new service account
    - Name: kachery-service-account (if you want)
    - Grant access to project: Role: Storage Object Admin
* Get the access keys for this service account
    - Navigate to Cloud storage
    - Click Settings (left Panel)
    - Interoperability
    - Create a key for a service account
    - Select the new service account
    - Copy the "Access Key" and the "Secret" and paste them somewhere temporary and safe. Note that once you close this box, you won't be able to retrieve the secret key ever again, but you can always create a new key pair.

## Example CORS configuration

```json
[
    {
      "origin": [
        "https://figurl.org", "https://www.figurl.org", "http://localhost:3000", "http://localhost:3001"
      ],
      "method": ["GET", "HEAD", "PUT"],
      "responseHeader": ["*"],
      "maxAgeSeconds": 3600
    }
]
```
