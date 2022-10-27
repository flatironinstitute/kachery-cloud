# Creating a Kachery Zone

This guide will show how to set up your own Kachery zone which will allow you to host Kachery files on resources that you manage. Note that the final step is to notify us so that your zone can be added to the global configuration.

## Choosing a name

Since the name of the zone cannot be changed later and will be visible to users, you should consult with us about choosing an appropriate name.

Let's assume the name of the new zone will be `zn1`. In the instructions below, replace `zn1` with the name of your zone.

## Create two storage buckets

The first step is to create two storage buckets, one for shared Kachery files (public) and one for admin files (private).

Here we assume that you are using Wasabi to create the buckets. (Instructions for creating Google or AWS buckets can be found elsewhere.)

* [Create public Wasabi bucket](./create_public_wasabi_bucket.md) - name: `kachery-zone-zn1`
* [Create private Wasabi bucket](./create_private_wasabi_bucket.md) - name: `kachery-zone-zn1-admin`

## Create a Google Cloud Project and a Firestore database

The Firestore database is used to Kachery client IDs and the associate users IDs, as well as some meta data for the stored files.

* Log into the Google cloud console: https://console.cloud.google.com
* Create a new project called `kachery-zone-zn1`
* Make sure the newly created project is selected in the console
* Create a Firestore database for the project
    - Select "Native Mode"
    - Choose a region

## Get credentials for default service account

In order for the serverless API to have access to the Firestore database, you will need to create access credentials.

* Navigate to APIs & Services -> Credentials
* Click on the default service account toward the bottom under "Service Accounts"
* Click the KEYS tab and click "ADD KEY -> Create New Key" and save the JSON file somewhere secret
* You'll need this below when setting up the serverless API

## Create a Google API key and Client ID

To allow users to log in to the website for this zone, for example to register a Kachery client, you will need to create a Google API key and Client ID for this project.

* APIs & Services -> Credentials
* Create Credentials -> API Key
    - Copy the API key for use in env variable below
* Configure consent screen
    - External
    - Leave most fields blank, use your email address for contact info
    - App name: `kachery-zone-zn1`
    - Authorize domain: `kachery-gateway-zn1.vercel.app`
    - Add a non-sensitive scope: `.../auth/userinfo.email`
    - Don't add any test users
    - Back to dashboard
    - Publish App
* Create Credentials -> OAuth client ID
    - Application type: Web application
    - Name: `kachery-gateway-client` (doesn't need to be globally unique)
    - Authorized javascript origins: `https://kachery-gateway-zn1.vercel.app`, `http://localhost:3000`, `http://localhost:3001`
    - Copy client ID for use in env variable below (the client secret is not actually needed)

## Create a reCAPTCHA site

To prevent abuse on the serverless API, we need to require that the sensitive website actions be initiated by a human.

* Go to https://www.google.com/recaptcha/admin and log in with your Google account
* Create a new reCAPTCHA site
* In settings, add the following domains: `kachery-zone-zn1.vercel.app`, `localhost`
* Copy the reCAPTCHA keys (site key and secret key)

## Host the serverless API with vercel

Kachery clients will communicate with your Kachery zone via a serverless API which will be hosted on [Vercel](https://vercel.com). You will need to set up for the deployment on your local system.

Prerequisites
* Linux or Mac
* nodeJS >= 16
* yarn
* [Vercel command-line interface](https://vercel.com/docs/cli)

Create an account on [Vercel](https://vercel.com)

On your local system, clone [kachery-gateway](https://github.com/scratchrealm/kachery-gateway) to a directory called `kachery-gateway-zn1`

```bash
git clone https://github.com/scratchrealm/kachery-gateway kachery-gateway-zn1
```

cd to `kachery-gateway-zn1` and run `yarn install`

```bash
cd kachery-gateway-zn1
yarn install
```

Run `vercel dev` and set up a new project called `kachery-gateway-zn1` (use the default settings)

`Ctrl+C` to exit out of dev server


Go to the vercel admin console on vercel.com, select the project, and set environment variables (Project -> Settings->Environment Variables):
* BUCKET_URI: `wasabi://kachery-zone-zn1?region=us-east-1` (assuming a Wasabi bucket in the us-east-1 region)
- BUCKET_CREDENTIALS: `{"accessKeyId":"...","secretAccessKey":"..."}` (obtained when creating the public bucket)
- ADMIN_BUCKET_URI: `wasabi://kachery-zone-zn1-admin?region=us-east-1` (assuming a Wasabi bucket in the us-east-1 region)
- ADMIN_BUCKET_CREDENTIALS: `{"accessKeyId":"...","secretAccessKey":"..."}` (same as bucket credentials if both were obtained from Wasabi)
- REACT_APP_RECAPTCHA_KEY
- RECAPTCHA_SECRET_KEY
- REACT_APP_ADMIN_USERS: ["you@gmail.com"] (replace with your Google email)
- REACT_APP_GOOGLE_API_KEY
- REACT_APP_GOOGLE_CLIENT_ID
- GOOGLE_CREDENTIALS (the contents of the file downloaded when creating a key for the Google service account)
* Deploy vercel app: `vercel --prod`
    - Check that deployed site is: https://kachery-gateway-zn1.vercel.app
* Visit the gateway website in browser
    - https://kachery-gateway-zn1.vercel.app

## Notify us

You'll need to notify us about the new zone so we can add it to the global configuration.

## Test the new zone

Set the following environment variable for all the below commands

```
export KACHERY_ZONE=zn1
```

Register your Kachery client on your local system

```bash
kachery-cloud-init
# This should direct you to a url within `https://kachery-gateway-zn1.vercel.app`
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

On Github, Create a new empty public github repo called `kachery-gateway-zn1`.

Add the new remote and push the main branch

```bash
git remote add zone https://github.com/<user>/kachery-gateway-zn1.git

git push zone main:main
```

Look at the contents of `.vercel/project.json` to get the vercel `projectId` and `orgId`. You will need those in the environment variables below.

Obtain a [vercel access token](https://vercel.com/guides/how-do-i-use-a-vercel-api-access-token).

On Github, open your project and go to Settings -> Secrets -> Actions. Add the following repository secrets:

```
VERCEL_PROJECT_ID: from above
VERCEL_ORG_ID: from above
VERCEL_TOKEN: from above
GOOGLE_CREDENTIALS: same as for vercel project
ADMIN_BUCKET_URI: same as for vercel project
ADMIN_BUCKET_CREDENTIALS: same as for vercel project
```

## Update the deployment

When the kachery-gateway software has been updated, do the following to deploy the updates

```bash
cd kachery-gateway-zn1

# Download the updates from the remote repo
git remote update origin

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
