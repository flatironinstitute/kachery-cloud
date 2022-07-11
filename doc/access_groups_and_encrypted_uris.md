## Access groups and encrypted URIs

The simplest way to share via kachery-cloud is

```python
uri = kcl.store_file(...)
```

and then share the URI or save it in a database. The file is stored in the configured project, which points to a slice of a cloud storage bucket. The file will be available semi-permanently until the project is deleted, or the bucket is decommissioned.

One issue with this is that all files are public. The only way to restrict access is to keep the URIs private. Access groups address this issue by encrypting URIs using kachery-cloud *access groups*.

Access groups can be created and managed using the [kachery-cloud web app](https://cloud.kacheryhub.org) and are owned and maintained by kachery-cloud users. Each access group has an ID, a label (for display), and the configurable access rules (including a list of authorized google IDs). The access group also has a secret key (readable by nobody) that is used to encrypt/decrypt content hashes via a web service.

Kachery-cloud URIs can be encrypted using the desired access group and then shared. The files cannot be retrieved unless the user has proper permissions according to the access group.

Here is an example of using encrypted URIs with access groups:

```python
import kachery_cloud as kcl

access_group = 'kddvtdrlrl' # The ID of the access group maintained at cloud.kacheryhub.org
uri = kcl.store_text('some-text '*3, label='some_text.txt')
uri_enc = kcl.encrypt_uri(uri, access_group=access_group)

print(uri)
print(uri_enc)

txt2 = kcl.load_text(uri_enc)
print(txt2)

# The output is:
# sha1://cbb44480e2918cb41791366d748294bdbb874b52?label=some_text.txt
# sha1-enc://4dc5679dfcd586c5e211cfad3699505d36f9dd8c275b8c6e67c94674ad8bcda3bc8af5a571a38120dff3570af057f957.ag_kddvtdrlrl?label=some_text.txt
# some-text some-text some-text 
```

The second URI is the encrypted one. That can be safely shared or stored in a public database.

### Advantages

Unlike the traditional use of encryption for restricting access, the files themselves are not encrypted. Thus we can revoke access without neeeding to re-upload files or change encryption keys.

### Caveats

The only way to share a file in multiple access groups is to create multiple (differently-encrypted URIs).

There is a bit of overhead in loading files with encrypted URIs because there is an extra decryption step required (an extra round-trip http request). In the future we will make this more efficient by combining steps, but we recommend that you only use encrypted URIs when needed.

If an access group is deleted, all the published URIs no longer function. Therefore it is important to keep track of which access groups are in use and should not be deleted.