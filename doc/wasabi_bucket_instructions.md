# Configuring a Wasabi bucket for use with kachery-cloud

Guide outline

* Create an account and sign to [wasabi.com](https://wasabi.com/)
    - You will need to create a paid account to enable public access to the bucket (required)
* Create a new bucket
    - The bucket name is globally unique
    - Pay attention to the region you choose (I don't think you can modify that later)
    - You can use all default options
* Allow public access
    - Navigate to the bucket
    - Click the settings icon to open settings for the bucket
    - Public access override
    - Enable public access
* Allow public reading of objects
    - Navigate to bucket settings
    - Policies tab
    - Use the example policy below, replacing `your-bucket-name`
* Get access keys
    - Wasabi console home
    - Access keys (left panel)
    - Create new access key
    - Copy the "Access Key" and the "Secret Key" and paste them somewhere temporary and safe. Note that once you close this box, you won't be able to retrieve the secret key ever again, but you can always create a new key pair.
* Register the bucket on kachery cloud
    - Navigate to https://cloud.kacheryhub.org/ and log in
    - Navigate to buckets and create a new bucket
    - Bucket label: match the Wasabi bucket name if you want
    - Bucket service: Wasabi
    - Bucket name: the name of the Wasabi bucket
    - Add the bucket
    - Edit the bucket credentials
    - Paste in the region code for the Wasabi bucket (e.g., us-east-1)
    - Paste in the Access Key ID and the Secret Access Key from above
    - Submit to add the bucket
* Register a new project on kachery cloud
    - Navigate to https://cloud.kacheryhub.org/ and log in
    - Navigate to projects and create a new project
    - Choose a name (e.g., the bucket name)
    - Choose the bucket from the dropdown
    - Add the project
* Set this as the default project for your kachery-cloud client
    - Navigate to https://cloud.kacheryhub.org/ and log in
    - Navigate to clients and select your client (if doesn't exist yet, use `kachery-cloud-init` from your computer)
    - Set the default project to the new project
    - The client should now be using the new bucket by default
* Test the configuration
    - TODO: not sure the best way to test this
* Phew
    - You did it!

## Example policy

> Important: replace `your-bucket-name`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPublicRead",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```