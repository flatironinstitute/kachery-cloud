# Configuring an AWS bucket for use with kachery-cloud

Guide outline

* Create an account and sign in to the [AWS Management Console](https://aws.amazon.com/console/)
* Navigate to S3 Buckets and create a new bucket
    - The bucket name is globally unique
    - Pay attention to the region you choose (I don't think you can modify that later)
    - Uncheck "Block all public access: because we want the bucket to be public
    - Otherwise, you can use the default options
* Allow public reading of objects
    - Navigate to the bucket Permissions tab
    - Edit the bucket Policy and use the AWS Policy generator
    - Type of policy: S3 Bucket Policy
    - Effect: Allow
    - Principal: *
    - Actions: GetObject
    - Amazon Resource Name: arn:aws:s3:::your-bucket-name/* (replace your-bucket-name)
    - Add the statement, generate the policy, and paste it in to where you are editing the bucket policy
    - Save changes to the bucket policy
* If you are going to use figurl, set up Cross-origin resource sharing (CORS)
    - Navigate to the bucket Permissions tab
    - Edit the CORS configuration
    - Paste in the example CORS configuration from below
* Create a policy for kachery access
    - Navigate to IAM Policies
    - Create a new policy
    - Service: s3
    - Actions: All S3 actions
    - Resources: bucket: Add ARN: `arn:aws:s3:::your-bucket-name` (replace)
    - Next: Next
    - Policy name: `kachery_access`
    - Create policy
* Create a user for kachery access
    - Navigate to IAM Users
    - Add a user
    - User name: kachery
    - Access type: Access key
    - Next: Permissions
    - Attach existing policies directly
    - Attach the kachery_access policy
    - Next: Next
    - Create user
* Get the access keys for the kachery user
    - Navigate to IAM Users
    - Navigate to the kachery user
    - Security credentials tab
    - Create access key
    - Copy the "Access Key ID" and the "Secret access key" and paste them somewhere temporary and safe. Note that once you close this box, you won't be able to retrieve the secret key ever again, but you can always create a new key pair.
* Register the bucket on kachery cloud
    - Navigate to https://cloud.kacheryhub.org/ and log in
    - Navigate to buckets and create a new bucket
    - Bucket label: match the AWS bucket name if you want
    - Bucket service: AWS
    - Bucket name: the name of the AWS bucket
    - Add the bucket
    - Edit the bucket credentials
    - Paste in the region code for the AWS bucket (e.g., us-east-1)
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

## Example CORS configuration
You may want to be more specific and target just `figurl.org` and `www.figurl.org`

```json
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "HEAD",
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```
