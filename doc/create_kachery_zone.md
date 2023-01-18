# Creating a Kachery Zone

This guide will show you how to set up your own Kachery zone (essentially a cloud storage bucket) which will allow you to host Kachery files on resources that you manage. You will need to register your zone with a gateway (coordinate with a gateway owner, or host your own gateway). A gateway is the infrastructure needed for the communication between Kachery clients and Kachery zones, with each gateway serving one or multiple zones.

Kachery zones are relatively low cost, particularly when the amount of data stored is below 1 TB. When using Cloudflare as the service provider, a bill for light usage would be less than $15/month. Cloudflare does not charge for network egress (download bandwidth) which provides a potentially large cost advantage compared with other services that charge on the order of $100/TB.

Here are the steps for creating a zone:
* [Choose a name](#choose-a-name)
* [Create a storage bucket](#create-a-storage-bucket)
* [Register your zone with a gateway](#register-your-zone-with-a-gateway)
* [Test the new zone](#test-the-new-zone)

## Choose a name

Before proceeding with the instructions below, please consult with us about an appropriate name for your zone. Since figURLs generated in your zone will have the name embedded, it may not be easy to change it later. Note that names need to be globally unique across the Kachery system, so it may be advisable to add a lab- or institution-specific prefix.

Let's assume that the name of the new zone is `example`. Whenever you see `example` in the instructions below, replace it with the name of your zone.

## Create a storage bucket

The first step is to create a storage bucket.

Each Kachery zone has a single storage bucket for storing content-addressable files and other information necessary for the functioning of the zone. Storage buckets are like file systems in the cloud, but instead of files and folders, buckets contain data objects. Here we assume that you are using [Cloudflare R2](https://www.cloudflare.com/lp/pg-r2/) which is the recommended method. (Instructions for creating Google, AWS, or Wasabi buckets will be provided at a later time.)

* [Create Cloudflare R2 bucket](./create_cloudflare_bucket.md) - name: `kachery-zone-example`

(The bucket name is not required to match the zone name; we follow a convention of building the bucket name by adding a `kachery-zone-` prefix to the name of the zone itself.)

## Register your zone with a gateway

As described above, each zone needs to be registered with a gateway. You will need to coordinate with a gateway owner. Send them the following information in a secure way, through a secure messaging service approved by your institution. (Email is typically not a secure way to transmit passwords or other important credentials.)

* Your zone name (e.g. `example`)
* The cloud storage provider (e.g., Cloudflare)
* The region of the bucket ("auto" for Cloudflare)
* The bucket name (e.g., `kachery-zone-example`)
* If using Cloudflare, the endpoint URL (obtained when setting up the bucket)
* Access Key ID and the Secret Access Key (obtained when setting up the bucket)

## Test the new zone

Once the gateway owner has notified you that the zone has been registered, set the following environment variable for all the below commands:

```
# replace "example" with your zone name
export KACHERY_ZONE=example
```

Register your local Kachery client:

```bash
kachery-cloud-init
# This should direct you to a URL where you will associate your local client with a GitHub user
```

Try storing a file and retrieving it:

```bash
echo "test-content" > test_content.txt
kachery-cloud-store test_content.txt
# sha1://b971c6ef19b1d70ae8f0feb989b106c319b36230?label=test_content.txt

kachery-cloud-cat sha1://b971c6ef19b1d70ae8f0feb989b106c319b36230?label=test_content.txt
# test-content

# verify that it's finding it in the new bucket
kachery-cloud-load-info sha1://b971c6ef19b1d70ae8f0feb989b106c319b36230?label=test_content.txt

# check that the bucketUri field in this output matches the zone
```
