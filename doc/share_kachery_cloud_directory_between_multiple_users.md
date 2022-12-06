## Sharing the kachery cloud directory between multiple users

On a shared system, you may want to share your kachery cloud directory between multiple users. To enable this, follow these steps:

**Create a new kachery cloud directory in a location where the users may access it with read and write permissions.**

For example, this could be on a shared drive.

**Have each user set the KACHERY_CLOUD_DIR environment variable to point to this directory on their system**

See above.

**Create a new UNIX group for users with access.**

Let's assume the name of the group is `testshare`. Add all the desired users to this group.

**Change the group ownership of all files in the kachery-cloud directory**

```bash
chgrp -R testshare $KACHERY_CLOUD_DIR
```

**Set the SGID bit for all directories**

Set the SGID bit set on all directories. With this set, all new files and directories will inherit the group ownership.

```bash
chmod g+s $KACHERY_CLOUD_DIR
find $KACHERY_CLOUD_DIR -type d -print0 | xargs -0 -n1 chmod g+s
```

**Set file permissions so that group members can read/write the files**

```bash
chmod -R g+rw $KACHERY_CLOUD_DIR
```

**Now, all users in `testgroup` will be able to use kachery-cloud with the same client directory**