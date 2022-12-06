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
* [Creating your own Kachery zone](./doc/create_kachery_zone.md)
* [Access groups and encrypted URIs](#access-groups-and-encrypted-uris)
* [Notes](#notes)

## Overview

Kachery-cloud is a network for sharing scientific data files between lab computers and [browser-based user interfaces](https://github.com/flatironinstitute/figurl). Resources are are accessed via registered Python clients or by web applications. Using simple Python commands you can store [files](doc/store_load_data.md) and [data objects](doc/store_load_data.md), and then retrieve or access these on a remote machine (or in a browser via JavaScript) by referencing universal URI strings. Kachery URIs are essentially content hashes, thus forming a [content-addressable storage database](./doc/content_addressable_storage.md). While the primary purpose of kachery-cloud at this time is to support [figurl](https://github.com/flatironinstitute/figurl), it can also be used independently in collaborative scientific research workflows for improving scientific reproducibility and dissemination.

## Installation and setup

Kachery-cloud is often installed as a dependency of other projects, but there are times when you may want to use it stand-alone.

It is best to use a [conda environment](./doc/conda_environments.md) or a virtual environment.

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

# Set the KACHERY_ZONE environment variable to control
# which directory files are upload to and retrieved from.
# If unset, the default zone is used.
export KACHERY_ZONE="..."
```

It is recommend that you [set these variables](./doc//setting_environment_variables_in_bashrc.md) in your `~/.bashrc` file.

## Creating your own Kachery zone

[Creating your own Kachery zone](./doc/create_kachery_zone.md)

## Sharing the kachery cloud directory between multiple users

[Share the kachery cloud directory between multiple users](./doc/share_kachery_cloud_directory_between_multiple_users.md)

## Authors

Jeremy Magland and Jeff Soules, [Center for Computational Mathematics, Flatiron Institute](https://www.simonsfoundation.org/flatiron/center-for-computational-mathematics)

## License

Apache 2.0
