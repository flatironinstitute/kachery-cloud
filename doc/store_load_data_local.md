# Storing and loading data in the local cache

> :warning: This project is in alpha stage of development.

> **IMPORTANT**: This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.

## Storing data to the local cache

From command line

```bash
echo "test-content-local" > test_content.txt
kachery-cloud-store-local test_content.txt
# output:
# sha1://414c7409445a8712a5e5c55d5554c84a515bd7f0?label=test_content.txt
```

From Python

```python
import numpy as np
import kachery_cloud as kcl

uri1 = kcl.store_file_local('/path/to/filename.dat')

uri2 = kcl.store_text_local('example text', label='example')
# uri2 = "sha1://d9e989f651cdd269d7f9bb8a215d024d8d283688?label=example"

uri3 = kcl.store_json_local({'example': 'dict'}, label='example.json')
# uri3 = "sha1://d0d9555e376ff13a08c6d56072808e27ca32d54a?label=example.json"

array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int16)
uri4 = kcl.store_npy_local(array, label='example.npy')
# uri4 = "sha1://bb55205a2482c6db2ace544fc7d8397551110701?label=example.npy"

uri5 = kcl.store_pkl_local({'example': array}, label='example.pkl')
# uri5 = "sha1://20d178d5a1264fc3267e38ca238c23f3e2dcd5d2?label=example.pkl"
```

## Loading data from the local cache

From command line

```bash
kachery-cloud-load sha1://414c7409445a8712a5e5c55d5554c84a515bd7f0?label=test_content.txt
# output:
# /home/<user>/.kachery-cloud/sha1/41/4c/74/414c7409445a8712a5e5c55d5554c84a515bd7f0

# Or write the file to stdout
kachery-cloud-cat sha1://414c7409445a8712a5e5c55d5554c84a515bd7f0?label=test_content.txt
# output:
# test-content-local
```

From Python

```python
import kachery_cloud as kcl

local_fname = kcl.load_file('sha1://414c7409445a8712a5e5c55d5554c84a515bd7f0?label=test_content.txt')

text = kcl.load_text('sha1://d9e989f651cdd269d7f9bb8a215d024d8d283688?label=example')
# example text

x = kcl.load_json('sha1://d0d9555e376ff13a08c6d56072808e27ca32d54a?label=example.json')
# {'example': 'dict'}

y = kcl.load_npy("sha1://bb55205a2482c6db2ace544fc7d8397551110701?label=example.npy")
# [[1 2 3], [4 5 6]]

z = kcl.load_pkl("sha1://20d178d5a1264fc3267e38ca238c23f3e2dcd5d2?label=example.pkl")
# {'example': array([[1, 2, 3], [4, 5, 6]], dtype=int16)}
```