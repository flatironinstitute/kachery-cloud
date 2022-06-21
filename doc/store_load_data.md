# Storing and loading data in the kachery cloud

> :warning: This project is in BETA.

> **IMPORTANT**: This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.

## Storing data

From command line

```bash
echo "test-content" > test_content.txt
kachery-cloud-store test_content.txt
# output:
# sha1://b971c6ef19b1d70ae8f0feb989b106c319b36230?label=test_content.txt
```

From Python

```python
import numpy as np
import kachery_cloud as kcl

uri1 = kcl.store_file('/path/to/filename.dat', cache_locally=True)

uri2 = kcl.store_text('example text', label='example.txt')
# uri2 = "sha1://d9e989f651cdd269d7f9bb8a215d024d8d283688?label=example.txt"

uri3 = kcl.store_json({'example': 'dict'}, label='example.json')
# uri3 = "sha1://d0d9555e376ff13a08c6d56072808e27ca32d54a?label=example.json"

array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int16)
uri4 = kcl.store_npy(array, label='example.npy')
# uri4 = "sha1://bb55205a2482c6db2ace544fc7d8397551110701?label=example.npy"

uri5 = kcl.store_pkl({'example': array}, label='example.pkl')
# uri5 = "sha1://20d178d5a1264fc3267e38ca238c23f3e2dcd5d2?label=example.pkl"
```

## Loading data

From command line

```bash
kachery-cloud-load sha1://b971c6ef19b1d70ae8f0feb989b106c319b36230?label=test_content.txt
# output:
# /home/<user>/.kachery-cloud/sha1/b9/71/c6/b971c6ef19b1d70ae8f0feb989b106c319b36230

# Or write the file to stdout
kachery-cloud-cat sha1://b971c6ef19b1d70ae8f0feb989b106c319b36230?label=test_content.txt
# output:
# test-content
```

From Python

```python
import kachery_cloud as kcl

local_fname = kcl.load_file('sha1://b971c6ef19b1d70ae8f0feb989b106c319b36230?label=test_content.txt')

text = kcl.load_text('sha1://d9e989f651cdd269d7f9bb8a215d024d8d283688?label=example.txt')
# example text

x = kcl.load_json('sha1://d0d9555e376ff13a08c6d56072808e27ca32d54a?label=example.json')
# {'example': 'dict'}

y = kcl.load_npy("sha1://bb55205a2482c6db2ace544fc7d8397551110701?label=example.npy")
# [[1 2 3], [4 5 6]]

z = kcl.load_pkl("sha1://20d178d5a1264fc3267e38ca238c23f3e2dcd5d2?label=example.pkl")
# {'example': array([[1, 2, 3], [4, 5, 6]], dtype=int16)}
```

## Limitations and explanations

All uploaded data is publicly available, although a person needs to know the URI in order to download it.

Uploads are subject to some limits which will change over time during development. Right now, individual uploads are limited to 5 GiB.

How is this free? By default, we use very inexpensive storage on the distributed web. Those who plan to store large amounts of data, or who want greater control of their data, should configure their own storage buckets (Google, AWS, Wasabi, or Filebase).

If you plan to use our freely-available storage space, you should be aware that uploaded files are not guaranteed to be available forever.