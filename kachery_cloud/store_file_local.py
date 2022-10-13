import os
import json
import hashlib
import shutil
import random
from tempfile import TemporaryDirectory
from urllib.parse import quote
from typing import Union
from .get_kachery_cloud_dir import get_kachery_cloud_dir
from .mutable_local import get_mutable_local, set_mutable_local
from ._sha1_of_string import _sha1_of_string
from ._fs_operations import _makedirs, _chmod_file


def store_file_local(filename: str, *, label: Union[str, None]=None, reference: Union[bool, None]=None):
    from .load_file import load_file
    if filename.startswith('sha1://'):
        filename = load_file(filename)
    if not os.path.isabs(filename):
        filename = os.path.abspath(filename)
    sha1 = _compute_file_hash(filename, algorithm='sha1')
    uri = f'sha1://{sha1}'
    if label is not None:
        uri = f'{uri}?label={quote(label)}'
    if reference:
        delim = '&' if '?' in uri else '?'
        uri = f'{uri}{delim}location={filename}'
        return uri
    kachery_cloud_dir = get_kachery_cloud_dir()
    kachery_storage_parent_dir = f'{kachery_cloud_dir}/sha1/{sha1[0]}{sha1[1]}/{sha1[2]}{sha1[3]}/{sha1[4]}{sha1[5]}'
    kachery_storage_file_name = f'{kachery_storage_parent_dir}/{sha1}'
    if not os.path.exists(kachery_storage_file_name):
        if not os.path.exists(kachery_storage_parent_dir):
            _makedirs(kachery_storage_parent_dir)
        tmp_filename = f'{kachery_storage_file_name}.{_random_string(10)}'
        shutil.copyfile(filename, tmp_filename)
        try:
            os.rename(tmp_filename, kachery_storage_file_name)
            # _chmod_file(kachery_storage_file_name)
        except:
            # Maybe another client renamed the file
            if not os.path.exists(kachery_storage_file_name):
                raise Exception(f'Unexpected problem renaming file: {tmp_filename} {kachery_storage_file_name}')
    return uri

def store_json_local(obj, *, label: Union[str, None]=None):
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/tmp.json'
        with open(fname, 'w') as f:
            json.dump(obj, f)
        return store_file_local(fname, label=label)

def _compute_file_hash(path: str, algorithm: str) -> str:
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    if not os.path.exists(path):
        raise Exception(f'File does not exist: {path}')
    size0 = os.path.getsize(path)
    if size0 > 1000 * 1000:
        a = get_mutable_local(f'@compute_sha1_cache/{_sha1_of_string(path)}')
        if a:
            a = json.loads(a)
            mtime = os.stat(path).st_mtime
            if a['size'] == size0 and a['mtime'] == mtime:
                return a['sha1']
    if (size0 > 1000 * 1000 * 100):
        print('Computing {} of {}'.format(algorithm, path))
    BLOCKSIZE = 65536
    hashsum = getattr(hashlib, algorithm)()
    with open(path, 'rb') as file:
        buf = file.read(BLOCKSIZE)
        while len(buf) > 0:
            hashsum.update(buf)
            buf = file.read(BLOCKSIZE)
    ret = hashsum.hexdigest()
    if size0 > 1000 * 1000:
        set_mutable_local(f'@compute_sha1_cache/{_sha1_of_string(path)}', json.dumps({
            'path': path,
            'size': size0,
            'mtime': os.stat(path).st_mtime,
            'sha1': ret
        }))
    return ret

def _random_string(num_chars: int) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(num_chars))