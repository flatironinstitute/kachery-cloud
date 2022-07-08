# Sharing local files with deferred upload (experimental)

Sometimes you may want to share a large number of files, but not upload them immediately to kachery-cloud, but rather upload on demand when they are requested.

To store files locally (and not upload immediately):

```bash
# Create a copy
kachery-cloud-store-local <path>

# Link to existing file
kachery-cloud-link <path>
```

Share all of your local files (allow them to be requested):

```bash
kachery-cloud-share-local-files-experimental
```

This will run a backend service which listens for file requests. When a file is requested, it is uploaded to the kachery cloud.

Keep this service running and make note of the printed project ID.

On a different computer, files can be requested via:

```bash
kachery-cloud-request-file-experimental <URI> --project <project-id>
```

This is also available in Python scripts:

```python
import kachery_cloud as kcl

# Run a file sharing backend
kcl.share_local_files_experimental()

# Store files locally
uri1 = kcl.store_file_local(path)
uri2 = kcl.store_text_local(text)
uri3 = kcl.store_json_local(obj0)
uri4 = kcl.store_npy_local(arr0)
uri5 = kcl.store_pkl_local(obj1)
uri7 = kcl.link_file(path)

# Request files from remote computer
path = kcl.request_file_experimental(uri, project_id='...')
text = kcl.request_text_experimental(uri, project_id='...')
obj0 = kcl.request_json_experimental(uri, project_id='...')
arr0 = kcl.request_npy_experimental(uri, project_id='...')
obj1 = kcl.request_pkl_experimental(uri, project_id='...')
```



