# Hosting a Kachery Gateway

The Kachery network is organized into gateways and zones, with each gateway serving one or more zones. A *zone* is essentially a cloud storage bucket (Cloudflare, AWS, Google, or Wasabi) and a *gateway* is the infrastructure needed for the communication between Kachery clients and the zones. Setting up a zone is a straightforward process. On the other hand, hosting a gateway requires signing up for and configuring several additional services; however, many users will not typically need to run their own gateways: you can coordinate with the owner of a gateway (such as the one maintained by the Flatiron Institute) to provide access to your zone. Be sure that you trust the gateway provider, as you will need to provide them with the credentials for the zone storage.

If you do wish to host your own Kachery gateway using cloud resources that you manage, this guide will describe how to do so. You will need to temporarily store some codes and passwords, so it is recommended that you create a temporary text file to store this information. Once the setup is complete, you should delete this file.

For some of the provisioned services, you will need to use a credit card to pay for the resources. Kachery gateways are relatively low cost. A bill for light usage could be as low as $25/month. [Here is an estimate](./kachery_gateway_cost_estimate.md) of the costs involved in hosting a gateway.

Here are the steps:
* [Create a MongoDB database](#create-a-mongodb-database)
* [Create a reCAPTCHA site](#create-a-recaptcha-site)
* [Set up a GitHub client for OAuth](#set-up-a-github-client-for-oauth)
* [Host the serverless API with Vercel](#host-the-serverless-api-with-vercel)
* [Set up GitHub actions](#set-up-github-actions)
* [Register new zones](#register-new-zones)
* [Update the deployment](#update-the-deployment)

Once your gateway is up and running you should periodically [update the deployment](#update-the-deployment) so that software updates can take effect.

## Create a MongoDB database

MongoDB is a NoSQL database that stores data in JSON-like documents. Each Kachery gateway requires access to a MongoDB database in order to store ephemeral data such as query caches and temporary logs.

* [Create Mongo Atlas database](./create_mongo_atlas_database.md)

## Create a reCAPTCHA site

To prevent abuse on the serverless API, you will need to ensure that the sensitive website actions are initiated by a human by configuring [reCAPTCHA](https://gist.github.com/magland/e1ffde94cff4f63a8cddb849a6b50637) for your gateway.

* Go to https://www.google.com/recaptcha/admin and log in with your Google account
* Create a new reCAPTCHA site
* In settings, add the following domains: `kachery-gateway-example.vercel.app`, `localhost`
* Copy the reCAPTCHA keys (site key and secret key) and store in a secure location

## Set up a GitHub client for OAuth

OAuth is an open standard for authorization that enables users to securely access resources without sharing passwords. Kachery uses OAuth to allow users to log in using GitHub to manage clients, zones, and other resources.

* Log in to GitHub go to [user settings](https://github.com/settings/profile)
* Scroll down and click on "Developer Settings" on the left panel
* Click "OAuth Apps"
* Click "New OAuth App"
* In the below steps replace `example` with the chosen name of your gateway.
  * Note that we follow a convention where the Vercel app name is a `kachery-gateway-` prefix followed by the name of the gateway.
* For the name use `kachery-gateway-example`
* For the homepage URL use `https://kachery-gateway-example.vercel.app`
  * Note that this should match the domain added during the reCAPTCHA setup.
* For the authorized callback URL use `https://kachery-gateway-example.vercel.app/github/auth`
* Click "Register Application"
* Copy and save the Client ID for a later step
* Generate a new client secret and save it for a later step

## Host the serverless API with Vercel

Kachery clients will communicate with your Kachery gateway via a [serverless API](./serverless_functions.md) which will be hosted on [Vercel](https://vercel.com). You will need to stage the deployment on your local system.

Prerequisites
* Linux or Mac
* nodeJS >= 16
* yarn
* [Vercel command-line interface](https://vercel.com/docs/cli)

Create an account on [Vercel](https://vercel.com). 

On your local system, clone [kachery-gateway](https://github.com/scratchrealm/kachery-gateway) to a directory called `kachery-gateway-example` (replace `example` with the name of your gateway)

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

# Ctrl+C to exit out of dev server once it has finished loading
```

Go to the vercel admin console on vercel.com, select the project, and set environment variables (Project -> Settings->Environment Variables):
- REACT_APP_RECAPTCHA_KEY (obtained when configuring the reCAPTCHA site)
- RECAPTCHA_SECRET_KEY (obtained when configuring the reCAPTCHA site)
- REACT_APP_ADMIN_USERS: ["user"] (replace with your github user ID)
- MONGO_URI (obtained when creating the Mongo Atlas database)
- REACT_APP_GITHUB_CLIENT_ID (obtained when creating the GitHub OAuth client)
- GITHUB_CLIENT_SECRET (obtained when creating the GitHub OAuth client)
- GATEWAY_CONFIG (yaml configuration - do not set this until you are adding your first zone)

Deploy the vercel app:

```bash
vercel --prod
```

Check in the console output that deployed site is: https://kachery-gateway-example.vercel.app

Visit the gateway website in browser

For example, https://kachery-gateway-example.vercel.app

## Set up GitHub actions

GitHub actions are needed to automate the deployment to Vercel of new software updates, and to perform maintenance tasks such as processing log items and clearing out expired cache records.

On GitHub, Create a new empty public GitHub repo called `kachery-gateway-example`.

Add the new remote and push the main branch:

```bash
cd kachery-gateway-example

# add a remote called 'gateway' that points to your empty repo
git remote add gateway https://github.com/<user>/kachery-gateway-example.git

# push the contents of your local repo to the remote
git push gateway main:main
```

Look at the contents of `.vercel/project.json` to get the vercel `projectId` and `orgId`. You will need those in the environment variables below.

Obtain a [vercel access token](https://vercel.com/guides/how-do-i-use-a-vercel-api-access-token).

On Github, open your project and go to Settings -> Secrets -> Actions. Add the following repository secrets:

```
VERCEL_PROJECT_ID (from above)
VERCEL_ORG_ID (from above)
VERCEL_TOKEN (from above)
GATEWAY_CONFIG (same as for vercel project)
MONGO_URI (same as for vercel project)
```

You can check whether this is working properly by manually triggering one of the GitHub actions from the GitHub web console for your repository. In your repo, click Actions in the top bar, then click "Process log items" on the left bar, and click the button to "Run Workflow".

## Register new zones

When a zone owner wants to register their zone with your gateway you will need to collect information from them and then update the GATEWAY_CONFIG environment variable on Vercel and on GitHub. See [this page](./create_kachery_zone.md) for the list of items the zone owner should provide.

Update the GATEWAY_CONFIG variable on Vercel and on GitHub with the following yaml format

```yaml
zones:
    -
        name: example
        bucketUri: 'r2://kachery-zone-example' # for cloudflare
        bucketCredentials: '{"endpoint": "...", "accessKeyId": "...", "secretAccessKey": "..."}' # for cloudflare
    -
        ...
```

Then redeploy the gateway on Vercel.

You will also need to register zone in the global Kachery zone directory. Contact the Kachery maintainers for information how to do this.

**Configuring CORS for the zone**

[What is CORS?](https://gist.github.com/magland/1032f78dd866f07ce6a7a5dcc64e2b40)

In order for figurl.org to access files stored in the Kachery zone, you must configure Cross-Origin Resource Sharing (CORS) on the storage bucket associated with the zone. To do this for a Cloudflare bucket, follow these steps:

* Open the kachery-gateway GUI (link above)
* Log in using GitHub (user must be among the ADMIN_USERS configured above)
* Click on Admin and then the "Configuration" Tab
* Click on "Set Cloudflare bucket CORS"

**Configure the authorization settings**

* Open the kachery-gateway GUI (link above)
* Log in using GitHub (user must be among the ADMIN_USERS configured above)
* Click on Admin and then the "Authorization Settings" Tab
* Allow public uploads (for now) and click the "SAVE" button

## Update the deployment

Whenever the kachery-gateway software has been updated, you will need to deploy those updates. You can deploy the updates by doing the following periodically:

```bash
cd kachery-gateway-example

# Download the changes from the remote repo
git fetch origin

# Checkout the main branch
git checkout main

# Merge in the changes
git merge origin/main

# Push to your gateway on Github
git push gateway main:main

# Do the same for the deploy branch
# This will trigger the deployment
git checkout deploy
git merge origin/deploy
git push gateway deploy:deploy

# Switch back to the main branch.
git checkout main
```

Check GitHub to monitor the deployment action workflow.
