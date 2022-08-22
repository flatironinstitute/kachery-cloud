import os
import shutil
from typing import Union
from .get_kachery_cloud_dir import get_kachery_cloud_dir
from ._fs_operations import _makedirs, _chmod_file


def set_mutable_local(key: str, value: str):
    _assert_valid_key(key)
    kachery_cloud_dir = get_kachery_cloud_dir()
    file_name = f'{kachery_cloud_dir}/mutables/{key}'
    parent_dir = os.path.dirname(file_name)
    if not os.path.exists(parent_dir):
        _makedirs(parent_dir)
    with open(file_name, 'w') as f:
        f.write(value)
    # _chmod_file(file_name)

def _assert_valid_key(key: str):
    a = key.split('/')
    if len(a) < 1: raise Exception(f'Invalid mutable key: {key}')
    for i in range(len(a)):
        b = a[i]
        if i < len(a) - 1:
            if not b.startswith('@'):
                raise Exception(f'Invalid mutable key: {key}')
        else:
            if b.startswith('@'):
                raise Exception(f'Invalid mutable key: {key}')
        if b == '.' or b == '..':
            raise Exception(f'Invalid mutable key: {key}')

def _assert_valid_folder_key(key: str):
    a = key.split('/')
    if len(a) < 1: raise Exception(f'Invalid mutable folder key: {key}')
    for i in range(len(a)):
        b = a[i]
        if not b.startswith('@'):
            raise Exception(f'Invalid mutable folder key: {key}')
        if b == '.' or b == '..':
            raise Exception(f'Invalid mutable folder key: {key}')

def get_mutable_local(key: str, default_value: Union[None, str]=None):
    _assert_valid_key(key)
    kachery_cloud_dir = get_kachery_cloud_dir()
    file_name = f'{kachery_cloud_dir}/mutables/{key}'
    if not os.path.exists(file_name):
        return default_value
    with open(file_name, 'r') as f:
        return f.read()

def delete_mutable_local(key: str):
    kachery_cloud_dir = get_kachery_cloud_dir()
    a = key.split('/')
    last_str = a[-1]
    if last_str.startswith('@'):
        raise Exception(f'Mutable key is a folder: {key}')
    else:
        _assert_valid_key(key)
        file_name = f'{kachery_cloud_dir}/mutables/{key}'
        if not os.path.exists(file_name):
            raise Exception(f'Mutable does not exist: {key}')
        os.unlink(file_name)

def delete_mutable_folder_local(key: str):
    kachery_cloud_dir = get_kachery_cloud_dir()
    a = key.split('/')
    last_str = a[-1]
    if last_str.startswith('@'):
        # deleting a folder
        _assert_valid_folder_key(key)
        folder_name = f'{kachery_cloud_dir}/mutables/{key}'
        if not os.path.exists(folder_name):
            raise Exception(f'Mutable folder does not exist: {key}')
        shutil.rmtree(folder_name)
    else:
        raise Exception(f'Not a mutable folder: {key}')

# def _add_snails(x: str):
#     # some/path/to/key -> @some/@path/@to/key
#     a = x.split('/')
#     for i in range(len(a) - 1):
#         a[i] = '@' + a[i]
#     return '/'.join(a)