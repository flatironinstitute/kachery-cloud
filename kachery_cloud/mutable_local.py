import os
from typing import Union
from .get_kachery_cloud_dir import get_kachery_cloud_dir
from ._fs_operations import _makedirs, _chmod_file


def set_mutable_local(key: str, value: str):
    assert _is_valid_key(key), f'Invalid mutable local key: {key}'
    kachery_cloud_dir = get_kachery_cloud_dir()
    file_name = f'{kachery_cloud_dir}/mutables/{_add_snails(key)}'
    parent_dir = os.path.dirname(file_name)
    if not os.path.exists(parent_dir):
        _makedirs(parent_dir)
    with open(file_name, 'w') as f:
        f.write(value)
    _chmod_file(file_name)

def _is_valid_key(key: str):
    a = key.split('/')
    for b in a:
        if b == '.' or b == '..':
            return False
        if b.startswith('@'):
            return False
    return True

def get_mutable_local(key: str, default_value: Union[None, str]=None):
    assert _is_valid_key(key), f'Invalid mutable local key: {key}'
    kachery_cloud_dir = get_kachery_cloud_dir()
    file_name = f'{kachery_cloud_dir}/mutables/{_add_snails(key)}'
    if not os.path.exists(file_name):
        return default_value
    with open(file_name, 'r') as f:
        return f.read()

def _add_snails(x: str):
    # some/path/to/key -> @some/@path/@to/key
    a = x.split('/')
    for i in range(len(a) - 1):
        a[i] = '@' + a[i]
    return '/'.join(a)