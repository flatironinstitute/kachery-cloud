from typing import Union, Any


# class ExampleCustomStorageBackend:
#     def __init__(self):
#         pass
#     def store_file(self, filename: str, *, label: Union[str, None] = None):
#         # upload to a bucket and return a url
#         ...

# resist the temptation to make a base class for inheritance
# we're just going to assume the _custom_storage_backend is an object
# with the store_file method that takes a filename and an optional label and returns a uri
_custom_storage_backend: Union[Any, None] = None

def set_custom_storage_backend(backend: Union[Any, None]):
    global _custom_storage_backend
    _custom_storage_backend = backend

def get_custom_storage_backend() -> Union[Any, None]:
    global _custom_storage_backend
    return _custom_storage_backend
