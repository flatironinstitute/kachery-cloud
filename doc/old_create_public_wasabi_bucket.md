# Creating a public Wasabi bucket as part of a Kachery zone

* Create an account and sign to [wasabi.com](https://wasabi.com/)
    - You will need to create a paid account to enable public access to the bucket
* Create a new bucket
    - The bucket name is globally unique (for example `kachery-zone-zn1`)
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