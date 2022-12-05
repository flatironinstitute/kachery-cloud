# Creating a Kachery Zone

This guide will show how to set up your own Kachery zone which will allow you to host Kachery files on resources that you manage. Note that the final step is to notify us so that your zone can be added to the global configuration.

During the setup process, you will need to temporarily store some codes and passwords, so it is recommended that you create a temporary text file to store this information. You should delete this file once the setup is complete.

## Choose a name

Since the name of the zone cannot be changed later and will be visible to users, you should consult with us about choosing an appropriate name.

Let's assume the name of the new zone will be `example`. Throughout the instructions below, replace `example` with the name of your zone.

## Create a storage bucket

The first step is to create a [storage bucket](./storage_bucket.md). Here we assume that you are using Cloudflare. (Instructions for creating Google, AWS, or Wasabi buckets can be found elsewhere.)

* [Create Cloudflare bucket](./create_cloudflare_bucket.md) - name: `kachery-zone-example`

## Create a MongoDB Atlas database

Each Kachery zone requires access to a [MongoDB database](./what_is_mongodb.md).

* [Create Mongo Atlas database](./create_mongo_atlas_database.md)

## Create a reCAPTCHA site

To prevent abuse on the serverless API, you will need to ensure that the sensitive website actions are initiated by a human by configuring [reCAPTCHA](./what_is_recaptcha.md) for your zone.

* Go to https://www.google.com/recaptcha/admin and log in with your Google account
* Create a new reCAPTCHA site
* In settings, add the following domains: `kachery-zone-example.vercel.app`, `localhost`
* Copy the reCAPTCHA keys (site key and secret key) and store in a secure location

## Set up a GitHub client ID for OAuth

[What is OAuth?](./what_is_oauth.md)

* Log in to GitHub go to [user settings](https://github.com/settings/profile)
* Scroll down and click on "Developer Settings" on the left panel

## Host the serverless API with vercel

Kachery clients will communicate with your Kachery zone via a serverless API which will be hosted on [Vercel](https://vercel.com). You will need to set up for the deployment on your local system.

Prerequisites
* Linux or Mac
* nodeJS >= 16
* yarn
* [Vercel command-line interface](https://vercel.com/docs/cli)

Create an account on [Vercel](https://vercel.com)

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
- BUCKET_CREDENTIALS: `{"accessKeyId":"...","secretAccessKey":"..."}` (obtained when creating the bucket)
- REACT_APP_RECAPTCHA_KEY (obtained when configuring the reCAPTCHA site)
- RECAPTCHA_SECRET_KEY (obtained when configuring the reCAPTCHA site)
- REACT_APP_ADMIN_USERS: ["user"] (replace with your github user ID)
- MONGO_URI (obtained when creating the Mongo Atlas database)
- REACT_APP_GITHUB_CLIENT_ID (obtained when creating the GitHub client)
- GITHUB_CLIENT_SECRET (obtained when creating the GitHub client)

Deploy the vercel app:

```bash
vercel --prod
```

Check that deployed site is: https://kachery-gateway-example.vercel.app

Visit the gateway website in browser

For example, https://kachery-gateway-example.vercel.app

## Configure CORS on the storage bucket

TODO

## Notify us

You'll need to notify us about the new zone so we can add it to the global configuration.

## Test the new zone

Set the following environment variable for all the below commands

```
export KACHERY_ZONE=example
```

Register your Kachery client on your local system

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
```

## Setting up Github actions

On Github, Create a new empty public github repo called `kachery-gateway-example`.

Add the new remote and push the main branch:

```bash
cd kachery-gateway-example

git remote add zone https://github.com/<user>/kachery-gateway-example.git

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

## Update the deployment

When the kachery-gateway software has been updated, do the following to deploy the updates

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

Check Github to monitor the deployment action.
