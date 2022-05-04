# Setting and getting mutables

> :warning: This project is in alpha stage of development.

> **IMPORTANT**: This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.

You can set and get mutables either in the cloud or on the local computer. Mutables stored in the cloud are specific to the configured kachery-cloud project.

Mutable keys are strings, resembling file paths. Mutable values are strings. It is often convenient to set a mutable value to be a URI.

## Setting mutables

```python
import kachery_cloud as kcl

uri1 = kcl.store_text('example text', label='example.txt')
kcl.set_mutable('test/key1', uri1)

uri2 = kcl.store_text('example text local', label='example.txt')
kcl.set_mutable_local('test/key1', uri2)
```

## Getting mutables

```python
import kachery_cloud as kcl

uri1 = kcl.get_mutable('test/key1')
txt1 = kcl.load_text(uri1)
# txt1 = "example text"

uri2 = kcl.get_mutable_local('test/key1')
txt2 = kcl.load_text(uri2)
# txt2 = "example text local"
```

## Limitations

This project is still in the alpha stage of development and we do not guarantee that your data will be available forever.