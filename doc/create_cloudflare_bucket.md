# Create a Cloudflare bucket as part of a Kachery zone

* Create an account and sign to [cloudflare.com](https://cloudflare.com/)
* Create a new bucket
    - Click "R2" in the left panel of the web console
    - Click "Create bucket"
    - Use automatic region and restricted access
* Get access credentials
    - Click "R2" on the left panel of the web console
    - Click "Manage R2 API Tokens" on the right side of the window
    - Click "Create API Token"
    - Allow edit permissions
    - Copy and save the Access Key ID and the Secret Access Key
        - Store them in a secure location
        - These will be needed later
    - Also copy and save the endpoint URL for the bucket
        - This is the URL toward the top of the bucket page, except don't include the zone name
        - So for example, you might see: `https://xxxxxxxxxxxxxxxxxxxx.r2.cloudflarestorage.com/kachery-zone-example`
        - In this, case the endpoint URL is: `https://xxxxxxxxxxxxxxxxxxxx.r2.cloudflarestorage.com`