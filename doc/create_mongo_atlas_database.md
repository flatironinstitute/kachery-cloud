# Create a Mongo Atlas database as part of a Kachery zone

* Create an account and sign to [mongodb.com](https://mongodb.com)
* Create a new database deployment
    - Click "Database" on the left panel in the web console
    - Click "Create" to create a database deployment
    - Select "Serverless" and AWS (or a different provider if you prefer)
    - Select Basic (not continuous) backup
    - For the name you can use `kachery-zone-example` (replace example with the name of your zone)
    - Wait a couple minutes for the deployment to be created
* Set up a user with access to the database
    - Click "Database Access" in the left panel
    - Click "Add new database user"
    - Select Password authentication method
    - For user name you can use `kachery-zone-example-user`
    - You can autogenerate a secure password (copy it and save it somewhere secure)
        - **important**: it will be easiest if the password does not have any special symbols, as they may need to be escaped later on when using the URI
    - Add a built-in role (read/write to any database)
    - Restrict access to specific clusters
        - Select the new deployment `kachery-zone-example`
    - Click to add the user
* Get the access uri (MONGO_URI)
    - Click "Database" on the left panel in the web console
    - Click "Connect" next to the `kachery-zone-example` deployment
    - Click "Connect your application"
    - Uncheck "Include full driver code example"
    - Copy the URI of the form `mongodb+srv://<username>:<password>@kachery-zone-example.xxxxx.mongodb.net/?retryWrites=true&w=majority`
    - Replace `<username>:<password>` with your user name and password
    - This is the MONGO_URI you will use when setting up your zone