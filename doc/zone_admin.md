# Administering a Kachery Zone

Once you have [created your kachery zone](./create_kachery_zone.md), you may wish to configure it.
Configuration, as well as usage monitoring, are available through the
[kachery-gateway](https://kachery-gateway.figurl.org) "Admin" tab.

At present, available zones are not exposed via the Internet; you will need
to create and visit a URL of the form
`https://kachery-gateway.figurl.org/admin?zone=YOUR_ZONE_HERE`
to administer your zone(s).

Note that the sidebar link will take you to the admin page of the default zone,
which you likely do not have permission to see!

## Usage Monitoring

The "Usage" tab provides the administrator with information about the extent of
usage of the kachery zone. For every kachery client which has accessed files in
the zone, it displays the owner (if known), and their total upload/download
statistics in both number of files and total bytes. "Fallback download" refers
to data transferred using the legacy data storage provider and will be removed
in a future version.

The top table shows all-time usage; if you scroll down the list, you can see
usage broken out by day.


## Configuration

Configuration management options for the zone itself (other than access control)
are located on the "Configuration" tab. The main purpose of this tab is to
allow the administrator to perform certain
maintenance tasks and tests.

### Variables List

This is a legacy display and will be removed in the future.

### Actions

This section allows the administrator to enable
[CORS](https://developer.mozilla.org/en-US/docs/Glossary/CORS)
for the storage bucket, in order to make its contents available to users.

For security reasons, this cannot be done programmatically, and must be
triggered by user action. However, it only needs to be done once per zone.

### Tests

These links allow the administrator to test the functionality of the storage
bucket and cache database, which can help diagnose issues in user access to
the kachery zone.


## Access Control

This tab allows you to manage who can interact with your kachery zone, and in what ways.

The relevant access controls are:

- **Public upload** -- off by default (only named users can upload files)
- **Public download** -- on by default (everyone can download a file if it is available)
- **User list** -- Individuals (identified via Github user name) who have greater
privileges than members of the public


### Authorization Settings

Access controls are managed through a `yaml` file, which can be edited using the
integrated editor on the "Authorization Settings" tab.

The file has three top-level keys:

- `allowPublicUpload`: set to `false` originally. If `true`, anyone can upload files.
- `allowPublicDownload`: set to `true` originally; if `false`, only named users can download files.
This is the setting that makes a zone private.
- `authorizedUsers`: A list of users, identified by Github user ID. For each user, possible keys are:
  - `userId`: Github user ID in quotes, e.g. `"happyUser"`
  - `upload`: `true` if the user is allowed to upload regardless of the `allowPublicUpload` setting.
  - `download`: `true` if the user is allowed to download regardless of the `allowPublicDownload` setting.
  May be safely omitted if public downloads are allowed.
  - `admin`: `true` if the user is allowed to have access to the admin page for this zone.

When you are satisfied with the changes to the YAML file, click the `save` button to persist them.
They will take effect once the file has been uploaded and parsed by the server.

The `save` button will be disabled if the `yaml` file contains syntax errors; however, it
is still possible to remove your own administrative privileges if you are careless. In
this event, you will need to contact the kachery-gateway administrators.
