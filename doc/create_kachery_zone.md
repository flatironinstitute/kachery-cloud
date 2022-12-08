# Creating a Kachery Zone

This guide will show you how to set up your own Kachery zone which will allow you to host Kachery files on resources that you manage. You will need to temporarily store some codes and passwords, so it is recommended that you create a temporary text file to store this information. Once the setup is complete, you should delete this file.

For some of the provisioned services, you will need to use a credit card to pay for the resources. Kachery zones are relatively low cost, particularly when the amount of data stored is below 10 TB. A bill for light usage could be as low as $25/month. [Here is an estimate](./kachery_zone_cost_estimate.md) of the costs involved in hosting a zone.

Here are the steps:
* [Choose a name](#choose-a-name)
* [Create a storage bucket](#create-a-storage-bucket)
* [Create a MongoDB database](#create-a-mongodb-database)
* [Create a reCAPTCHA site](#create-a-recaptcha-site)
* [Set up a GitHub client for OAuth](#set-up-a-github-client-for-oauth)
* [Host the serverless API with Vercel](#host-the-serverless-api-with-vercel)
* [Configure the zone](#configure-the-zone)
* [Notify us of the new zone](#notify-us-of-the-new-zone)
* [Test the new zone](#test-the-new-zone)

Once your zone is up and running you should periodically [update the deployment](#update-the-deployment) so that software updates can take effect.

## Choose a name

Before proceeding with the instructions below, please consult with us about an appropriate name for your zone. Since figURLs generated in your zone will have the name embedded, it may not be easy to change it later.

Let's assume that the name of the new zone is `example`. Whenever you see `example` in the instructions below, replace it with the name of your zone.

## Create a storage bucket

The first step is to create a storage bucket.

Each Kachery zone has a single storage bucket for storing content-addressable files and other information necessary for the functioning of the zone. Storage buckets are like file systems in the cloud, but instead of files and folders, buckets contain data objects. Here we assume that you are using [Cloudflare R2](https://www.cloudflare.com/lp/pg-r2/) which is the recommended method. (Instructions for creating Google, AWS, or Wasabi buckets can be found elsewhere.)

* [Create Cloudflare R2 bucket](./create_cloudflare_bucket.md) - name: `kachery-zone-example`

## Create a MongoDB database

MongoDB is a NoSQL database that stores data in JSON-like documents. Each Kachery zone requires access to a MongoDB database in order to store ephemeral data such as query caches and temporary logs.

* [Create Mongo Atlas database](./create_mongo_atlas_database.md)

## Create a reCAPTCHA site

To prevent abuse on the serverless API, you will need to ensure that the sensitive website actions are initiated by a human by configuring [reCAPTCHA](https://gist.github.com/magland/e1ffde94cff4f63a8cddb849a6b50637) for your zone.

* Go to https://www.google.com/recaptcha/admin and log in with your Google account
* Create a new reCAPTCHA site
* In settings, add the following domains: `kachery-zone-example.vercel.app`, `localhost`
* Copy the reCAPTCHA keys (site key and secret key) and store in a secure location

## Set up a GitHub client for OAuth

OAuth is an open standard for authorization that enables users to securely access resources without sharing passwords. Kachery uses OAuth to allow users to log in using GitHub to manage clients, zones, and other resources.

* Log in to GitHub go to [user settings](https://github.com/settings/profile)
* Scroll down and click on "Developer Settings" on the left panel
* Click "OAuth Apps"
* Click "New OAuth App"
* In the below steps replace `example` with the name of your zone.
* For the name use `kachery-gateway-example`
* For the homepage URL use `https://kachery-gateway-example.vercel.app`
* For the authorized callback URL use `https://kachery-gateway-example.vercel.app/github/auth`
* Click "Register Application"
* Copy and save the Client ID for a later step
* Generate a new client secret and save it for a later step

## Host the serverless API with Vercel

Kachery clients will communicate with your Kachery zone via a [serverless API](./serverless_functions.md) which will be hosted on [Vercel](https://vercel.com). You will need to stage the deployment on your local system.

Prerequisites
* Linux or Mac
* nodeJS >= 16
* yarn
* [Vercel command-line interface](https://vercel.com/docs/cli)

Create an account on [Vercel](https://vercel.com). 

On your local system, clone [kachery-gateway](https://github.com/scratchrealm/kachery-gateway) to a directory called `kachery-gateway-example` (replace `example` with the name of your zone)

```bash
git clone https://github.com/scratchrealm/kachery-gateway kachery-gateway-example
```

Install the npm packages for the project

```bash
cd kachery-gateway-example
yarn install
```

Set up a new Vercel project called `kachery-gateway-example` by running

```bash
vercel dev
# use the default settings

# Ctrl+C to exit out of dev server
```

Go to the vercel admin console on vercel.com, select the project, and set environment variables (Project -> Settings->Environment Variables):
* BUCKET_URI: `r2://kachery-zone-example`
- BUCKET_CREDENTIALS: `{"accessKeyId":"...","secretAccessKey":"...", "endpoint":"..."}` (obtained when creating the bucket)
- REACT_APP_RECAPTCHA_KEY (obtained when configuring the reCAPTCHA site)
- RECAPTCHA_SECRET_KEY (obtained when configuring the reCAPTCHA site)
- REACT_APP_ADMIN_USERS: ["user"] (replace with your github user ID)
- MONGO_URI (obtained when creating the Mongo Atlas database)
- REACT_APP_GITHUB_CLIENT_ID (obtained when creating the GitHub OAuth client)
- GITHUB_CLIENT_SECRET (obtained when creating the GitHub OAuth client)

Deploy the vercel app:

```bash
vercel --prod
```

Check that deployed site is: https://kachery-gateway-example.vercel.app

Visit the gateway website in browser

For example, https://kachery-gateway-example.vercel.app

## Configure the zone

**Configure CORS**

[What is CORS?](https://gist.github.com/magland/1032f78dd866f07ce6a7a5dcc64e2b40)

In order for figurl.org to access files stored in your Kachery zone, you must configure Cross-Origin Resource Sharing (CORS) on the storage bucket associated with your zone. To set up your Cloudflare bucket, follow these steps:

* Open the kachery-gateway GUI (link above)
* Log in using GitHub (user must be among the ADMIN_USERS configured above)
* Click on Admin and then the "Configuration" Tab
* Click on "Set Cloudflare bucket CORS"

**Configure the authorization settings**

* Open the kachery-gateway GUI (link above)
* Log in using GitHub (user must be among the ADMIN_USERS configured above)
* Click on Admin and then the "Authorization Settings" Tab
* Allow public uploads (for now) and click the "SAVE" button

## Notify us of the new zone

In order to proceed, you'll need to notify us about the new zone so we can add it to the global configuration. Tell us the zone name and the gateway URL (e.g., `https://kachery-gateway-example.vercel.app`).

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

## Set up GitHub actions

GitHub actions are needed to automate the deployment to Vercel of new software updates, and to perform maintenance tasks such as processing log items and clearing out expired cache records.

On GitHub, Create a new empty public github repo called `kachery-gateway-example`.

Add the new remote and push the main branch:

```bash
cd kachery-gateway-example

# add a remote called 'zone' that points to your empty repo
git remote add zone https://github.com/<user>/kachery-gateway-example.git

# push the contents of your local repo to the remote
git push zone main:main
```

Look at the contents of `.vercel/project.json` to get the vercel `projectId` and `orgId`. You will need those in the environment variables below.

Obtain a [vercel access token](https://vercel.com/guides/how-do-i-use-a-vercel-api-access-token).

On Github, open your project and go to Settings -> Secrets -> Actions. Add the following repository secrets:

```
VERCEL_PROJECT_ID (from above)
VERCEL_ORG_ID (from above)
VERCEL_TOKEN (from above)
BUCKET_URI (same as for vercel project)
BUCKET_CREDENTIALS (same as for vercel project)
MONGO_URI (same as for vercel project)
```

You can check whether this is working properly by manually triggering one of the GitHub actions from the GitHub web console for your repository. In your repo, click Actions in the top bar, then click "Process log items" on the left bar, and click the button to "Run Workflow".

## Update the deployment

Whenever the kachery-gateway software has been updated, you can deploy the updates by doing the following:

```bash
cd kachery-gateway-example

# Download the changes from the remote repo
git fetch origin

# Checkout the main branch
git checkout main

# Merge in the changes
git merge origin/main

# Push to your zone on Github
git push zone main:main

# Do the same for the deploy branch
# This will trigger the deployment
git checkout deploy
git merge origin/deploy
git push zone deploy:deploy

# Switch back to the main branch.
git checkout main
```

Check GitHub to monitor the deployment action workflow.
