import os
import hashlib
import shutil
import random
from urllib.parse import quote
from typing import Union
from .get_kachery_cloud_dir import get_kachery_cloud_dir


def store_file_local(filename: str, *, label: Union[str, None]=None):
    sha1 = _compute_file_hash(filename, algorithm='sha1')
    uri = f'sha1://{sha1}'
    if label is not None:
        uri = f'{uri}?label={quote(label)}'
    kachery_cloud_dir = get_kachery_cloud_dir()
    kachery_storage_parent_dir = f'{kachery_cloud_dir}/sha1/{sha1[0]}{sha1[1]}/{sha1[2]}{sha1[3]}/{sha1[4]}{sha1[5]}'
    kachery_storage_file_name = f'{kachery_storage_parent_dir}/{sha1}'
    if not os.path.exists(kachery_storage_file_name):
        if not os.path.exists(kachery_storage_parent_dir):
            os.makedirs(kachery_storage_parent_dir)
        tmp_filename = f'{kachery_storage_file_name}.{_random_string(10)}'
        shutil.copyfile(filename, tmp_filename)
        try:
            os.rename(tmp_filename, kachery_storage_file_name)
        except:
            # Maybe another client renamed the file
            if not os.path.exists(kachery_storage_file_name):
                raise Exception(f'Unexpected problem renaming file: {tmp_filename} {kachery_storage_file_name}')
    return uri

def _compute_file_hash(path: str, algorithm: str) -> str:
    if not os.path.exists(path):
        raise Exception(f'File does not exist: {path}')
    if (os.path.getsize(path) > 1024 * 1024 * 100):
        print('Computing {} of {}'.format(algorithm, path))
    BLOCKSIZE = 65536
    hashsum = getattr(hashlib, algorithm)()
    with open(path, 'rb') as file:
        buf = file.read(BLOCKSIZE)
        while len(buf) > 0:
            hashsum.update(buf)
            buf = file.read(BLOCKSIZE)
    return hashsum.hexdigest()

def _random_string(num_chars: int) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(num_chars))