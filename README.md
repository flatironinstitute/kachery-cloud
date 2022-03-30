# kachery-cloud

Frictionless cloud sharing of scientific research data using Python.

Note: This package is intended for the public sharing of scientific data for collaborative research. It should not be used for other purposes.

## Installation and setup

```bash
pip install --upgrade git+https://github.com/scratchrealm/kachery-cloud
```

To complete the setup, open a terminal and run 

```bash
# One-time initialization
kachery-cloud-init
```

Click on the link which will bring you to a page where you can log in with Google and associate this client with your Google user. This initialization only needs to be performed once on your computer. The client information will be stored in `~/.kachery-cloud`.

If you are using a colab or jupyter notebook and do not have easy access to a terminal, you can also run this step in the notebook:

```python
# One-time initialization (alternate method)
import kachery_cloud as kc
kc.init()
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
import kachery_cloud as kc

uri = kc.store_file('/path/to/filename.dat')
uri = kc.store_text('example text')
uri = kc.store_json({'example': 'dict'})
uri = kc.store_npy(array)
uri = kc.store_pkl({'example': array})
```

## Loading data

From command line

```bash
kachery-cloud-load ipfs://bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga
# output:
# /home/<user>/.kachery-cloud/ipfs/mp/n5/ga/bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga
```

From Python

```python
import kachery_cloud as kc

local_fname = kc.load_file('ipfs://bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga')
text = kc.load_text('ipfs://bafkreiajr6u7obg3mpunezz2mwarr2sptwr3zaedia665vdayvw6mpn5ga')
x = kc.load_json(uri)
y = kc.load_npy(uri)
z = kc.load_pkl(uri)
```

## Limitations

Uploads are subject to the limits of web3.storage (for example, no more than 30 uploads per 10 seconds).

If you are using our service for uploading to IPFS (not your own web3.storage token), then uploads are limited to 50 MiB and are not guaranteed to be available forever. Also, the upload rate may be throttled.
