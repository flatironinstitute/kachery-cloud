<img src="https://user-images.githubusercontent.com/3679296/161265718-1127dd6a-a7c4-419b-b9e0-915740c418bc.svg" width="400px" />

# kachery-cloud

> :warning: This project is in BETA.

> **IMPORTANT**: This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.

> **PLEASE NOTE**: At this point, uploaded files are not guaranteed to be available forever.

Share scientific research data in the cloud using Python.

Kachery-cloud is a core part of [figurl](https://github.com/flatironinstitute/figurl).

Contents

* [Overview](#overview)
* [Installation and setup](#installation-and-setup)
* [Basic usage](#basic-usage)
* [Environment variables](#environment-variables)
* [Creating your own Kachery zone](#creating-your-own-kachery-zone)
* [Sharing the kachery cloud directory between multiple users](#sharing-the-kachery-cloud-directory-between-multiple-users)
* [Access groups and encrypted URIs](#access-groups-and-encrypted-uris)
* [Notes](#notes)

## Overview

Kachery-cloud is a network for sharing scientific data files between lab computers and [browser-based user interfaces](https://github.com/flatironinstitute/figurl). Resources are are accessed via registered Python clients or by web applications. Using simple Python commands you can store [files](doc/store_load_data.md) and [data objects](doc/store_load_data.md), and then retrieve or access these on a remote machine (or in a browser via JavaScript) by referencing universal URI strings. Kachery URIs are essentially content hashes, thus forming a [content-addressable storage database](https://en.wikipedia.org/wiki/Content-addressable_storage). While the primary purpose of kachery-cloud at this time is to support [figurl](https://github.com/flatironinstitute/figurl), it can also be used independently in collaborative scientific research workflows and for improving scientific reproducibility and dissemination.

## Installation and setup

Kachery-cloud is often installed as a dependency of other projects, but there are times when you may want to use it stand-alone.

It is best to use a conda environment or a venv.

Requirements
* Python >= 3.8
* numpy

```bash
pip install kachery-cloud

# or for the development version, clone this repo and install via "pip install -e ."
```

To complete the setup, open a terminal and run 

```bash
# One-time initialization
kachery-cloud-init

# Follow the instructions to associate your computer with your Google user on the kachery-cloud network
```

Clicking the link will bring you to a page where you associate this account with a Google user ID for the purpose of managing projects and tracking usage. This initialization only needs to be performed once on your computer. The client information will be stored in `~/.kachery-cloud`.

If you are using a colab or jupyter notebook and do not have easy access to a terminal, you can also run this one-time step in the notebook:

```python
# One-time initialization (alternate method)
import kachery_cloud as kcl
kcl.init()

# Follow the instructions to associate the client with your Google user on the kachery-cloud network
```

## Basic usage

* [Storing and loading data in the kachery cloud](doc/store_load_data.md)
* [Storing and loading data in the local cache](doc/store_load_data_local.md)

## Environment variables

You can use an environment variables to control the storage/configuration directory used by kachery-cloud.

```bash
# Set the storage/configuration directory used by kachery-cloud
# If unset, $HOME/.kachery-cloud will be used
# The client ID will be determined by this directory
# You can share the same kachery-cloud directory between multiple users,
# but you will need to set mult-user mode for the client
export KACHERY_CLOUD_DIR="..."
```

It is recommend that you set this variable in your `~/.bashrc` file.

## Creating your own Kachery zone

[Creating your own Kachery zone](./doc/create_kachery_zone.md)

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

## Notes

This project is in the beta stage of development and we do not guarantee that your data will be available forever.

## Authors

Jeremy Magland and Jeff Soules, [Center for Computational Mathematics, Flatiron Institute](https://www.simonsfoundation.org/flatiron/center-for-computational-mathematics)

## License

Apache 2.0
