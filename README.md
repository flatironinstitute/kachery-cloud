# kachery-cloud

> :warning: This project is in alpha stage of development.

Share scientific research data on the distributed web using Python.

Note: This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.

## Installation and setup

It is best to use a conda environment or a venv.

Requirements
* Python >= 3.8
* numpy

```bash
pip install --upgrade git+https://github.com/scratchrealm/kachery-cloud
```

To complete the setup, open a terminal and run 

```bash
# One-time initialization
kachery-cloud-init

# Outputs a link to click on
```

Clicking the link will bring you to a page where you associate this account with a Google user ID for the purpose of managing projects and tracking usage. This initialization only needs to be performed once on your computer. The client information will be stored in `~/.kachery-cloud`.

If you are using a colab or jupyter notebook and do not have easy access to a terminal, you can also run this one-time step in the notebook:

```python
# One-time initialization (alternate method)
import kachery_cloud as kcl
kcl.init()
```

## Storing data

From command line

```bash
echo "test-content" > test_content.txt
kachery-cloud-store test_content.txt
# output:
# ipfs://bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga
```

From Python

```python
import numpy as np
import kachery_cloud as kcl

uri1 = kcl.store_file('/path/to/filename.dat')

uri2 = kcl.store_text('example text')
# uri2 = "ipfs://bafkreiaossxdnwtp6a4zfjl73w67i4ulmcoq277g5maz7kprxg23kqgygu"

uri3 = kcl.store_json({'example': 'dict'})
# uri3 = "ipfs://bafkreig3edwqihmsm2o7kts6v4cpvtfs66olgonclogykndsu4v7ordox4"

array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int16)
uri4 = kcl.store_npy(array)
# uri4 = "ipfs://bafkreihqe5oxpuc5rvsj2pq77exjb5llx5abhth4vhac7tc6mxlrbyt6em"

uri5 = kcl.store_pkl({'example': array})
# uri5 = "ipfs://bafkreihdk3qrmf4665bn7m72t2niah3lujblbcnlevly5l5mequnft6w3y"
```

## Loading data

From command line

```bash
kachery-cloud-load ipfs://bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga
# output:
# /home/<user>/.kachery-cloud/ipfs/mp/n5/ga/bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga

# Or write the file to stdout
kachery-cloud-cat ipfs://bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga
# output:
# test-content
```

From Python

```python
import kachery_cloud as kcl

local_fname = kcl.load_file('ipfs://bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga')

text = kcl.load_text('ipfs://bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga')
# example text

x = kcl.load_json('ipfs://bafkreig3edwqihmsm2o7kts6v4cpvtfs66olgonclogykndsu4v7ordox4')
# {'example': 'dict'}

y = kcl.load_npy("ipfs://bafkreihqe5oxpuc5rvsj2pq77exjb5llx5abhth4vhac7tc6mxlrbyt6em")
# [[1 2 3], [4 5 6]]

z = kcl.load_pkl("ipfs://bafkreihdk3qrmf4665bn7m72t2niah3lujblbcnlevly5l5mequnft6w3y")
# {'example': array([[1, 2, 3], [4, 5, 6]], dtype=int16)}
```

## Limitations and explanations

All uploaded data is publicly available on [IPFS](https://ipfs.io/), although a person needs to know the URI in order to download it.

Uploads are subject to some limits which will change over time during development. Right now, individual uploads are limited to 50 MiB.

How is this free? For now we use extremely inexpensive storage on the distributed web using [Filebase](https://filebase.com/). This service stores data on the [sia](https://sia.tech/) decentralized storage network and pins it to [IPFS](https://ipfs.io/).

If you plan to make heavy use of kachery cloud, or if you want greater control of your uploaded data, then you should create your own [Filebase](https://filebase.com/) account and configure your client to store data on your own bucket. See their [pricing model](https://docs.filebase.com/billing-and-pricing/pricing-model).

If you plan to use our freely-available storage space, you should be aware that uploaded files are not guaranteed to be available forever. You may want to pin the files to your own IPFS nodes (or use your own Filebase account) if you want them to stay available in the long term.