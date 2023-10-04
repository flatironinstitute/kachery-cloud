<img src="https://user-images.githubusercontent.com/3679296/161265718-1127dd6a-a7c4-419b-b9e0-915740c418bc.svg" width="400px" />

# kachery-cloud

> :warning: This project is in BETA.

> **IMPORTANT**: This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.

> **PLEASE NOTE**: At this point, uploaded files are not guaranteed to be available forever.

Kachery-cloud is designed to make it easier for researchers to share data and files between different computers and with web applications. It provides a content-addressable storage network and a uniform way to access data and files across different machines. The goal is to make scientific research more reproducible and collaborative.

Kachery-cloud is a core part of [figurl](https://github.com/flatironinstitute/figurl).

Contents

* [Overview](#overview)
* [Installation and setup](#installation-and-setup)
* [Basic usage](#basic-usage)
* [Environment variables](#environment-variables)
* [Hosting a Kachery zone](./doc/create_kachery_zone.md)
* [Hosting a Kachery resource](https://github.com/scratchrealm/kachery-resource/blob/main/README.md)
* [Hosting a Kachery gateway](./doc/host_kachery_gateway.md)
* [Administering a Kachery zone](./doc/zone_admin.md)
* [Frequenty asked questions](./doc/faq.md)
* [Authors](#authors)
* [License](#license)
## Overview

Kachery-cloud is a network designed for scientists to share files between lab computers and between workstations and [web browsers](https://github.com/flatironinstitute/figurl). Access to the network is granted through registered Python clients and web applications that [store and access files](doc/store_load_data.md) and [data objects](doc/store_load_data.md). Kachery URIs are essentially content hashes, and in this way, Kachery forms a [content-addressable storage database](https://gist.github.com/magland/e41b6c0823fe308c6e4176a54cfbdbe9). While a primary purpose of kachery-cloud is to support [figurl](https://github.com/flatironinstitute/figurl) in the browser, it can also be incorporated into scientific workflows in other ways to enhance reproducibility and dissemination.

## Installation and setup

Kachery-cloud is often installed as a dependency of other projects, but there are times when you may want to use it stand-alone.

It is best to use a [conda environment](https://gist.github.com/magland/7f3fecc6cdcd3fae99868c10f6b585c7) or a virtual environment.

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

# Follow the instructions to associate your computer with your GitHub user on the kachery-cloud network
```

Clicking the link will bring you to a page where you associate this account with a GitHub user ID for the purpose of managing projects and tracking usage. This initialization only needs to be performed once on your computer. The client information will be stored in `~/.kachery-cloud`.

If you are using a colab or jupyter notebook and do not have easy access to a terminal, you can also run this one-time step in the notebook:

```python
# One-time initialization (alternate method)
import kachery_cloud as kcl
kcl.init()

# Follow the instructions to associate the client with your GitHub user on the kachery-cloud network
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

It is recommend that you [set these variables](https://gist.github.com/magland/518945134209c0c13789c963efda482f) in your `~/.bashrc` file.

## Creating your own Kachery zone

[Creating your own Kachery zone](./doc/create_kachery_zone.md)

[Administering your Kachery zone](./doc/zone_admin.md)

## Hosting a Kachery resource

[Hosting a Kachery resource](https://github.com/scratchrealm/kachery-resource/blob/main/README.md)

# Hosting a Kachery gateway

[Hosting a Kachery gateway](./doc/host_kachery_gateway.md)

## Sharing the kachery cloud directory between multiple users

[Share the kachery cloud directory between multiple users](./doc/share_kachery_cloud_directory_between_multiple_users.md)


## Frequently asked questions

[Frequently asked questions](./doc/faq.md)

## Authors

Jeremy Magland and Jeff Soules, [Center for Computational Mathematics, Flatiron Institute](https://www.simonsfoundation.org/flatiron/center-for-computational-mathematics)

## License

Kachery-cloud is an open source project and released under the Apache 2.0 license.
