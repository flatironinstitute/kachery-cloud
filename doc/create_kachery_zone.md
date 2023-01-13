# Creating a Kachery Zone

This guide will show you how to set up your own Kachery zone (essentially a cloud storage bucket) which will allow you to host Kachery files on resources that you manage. You will need to register your zone with a gateway (you will need to coordinate with a gateway owner, or host your own gateway). A gateway is the infrastructure needed for the communication between Kachery clients and the zones, and each gateway serves one or multiple zones.

Kachery zones are relatively low cost, particularly when the amount of data stored is below 10 TB. A bill for light usage would be less than $15/month. [Here is an estimate](./kachery_zone_cost_estimate.md) of the costs involved in hosting a zone.

Here are the steps:
* [Choose a name](#choose-a-name)
* [Create a storage bucket](#create-a-storage-bucket)
* [Register your zone with a gateway](#register-your-zone-with-a-gateway)
* [Test the new zone](#test-the-new-zone)

## Choose a name

Before proceeding with the instructions below, please consult with us about an appropriate name for your zone. Since figURLs generated in your zone will have the name embedded, it may not be easy to change it later.

Let's assume that the name of the new zone is `example`. Whenever you see `example` in the instructions below, replace it with the name of your zone.

## Create a storage bucket

The first step is to create a storage bucket.

Each Kachery zone has a single storage bucket for storing content-addressable files and other information necessary for the functioning of the zone. Storage buckets are like file systems in the cloud, but instead of files and folders, buckets contain data objects. Here we assume that you are using [Cloudflare R2](https://www.cloudflare.com/lp/pg-r2/) which is the recommended method. (Instructions for creating Google, AWS, or Wasabi buckets can be found elsewhere.)

* [Create Cloudflare R2 bucket](./create_cloudflare_bucket.md) - name: `kachery-zone-example`

## Register your zone with a gateway

As described above, each zone needs to be registered with a gateway. You will need to coordinate with a gateway owner. Send them the following information in a secure way.

* Your zone name
* The cloud storage provider (e.g., Cloudflare)
* The region of the bucket ("auto" for Cloudflare)
* The bucket name (e.g., `kachery-zone-example`)
* If using Cloudflare, the endpoint URL (obtained when setting up the bucket)
* Access Key ID and the Secret Access Key (obtained when setting up the bucket)

In addition, to add your zone to the global directory, you will also need to send the name of your zone, and the URL of the gateway to the central gateway maintainers (the authors of this package). You can obtain the gateway URL from the gateway owner.

## Test the new zone

Set the following environment variable for all the below commands

```
# replace example with your zone name
export KACHERY_ZONE=example
```

Register your local Kachery client

```bash
kachery-cloud-init
# This should direct you to a url within `https://kachery-gateway-example.vercel.app`
```

Try storing a file and retrieving it

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