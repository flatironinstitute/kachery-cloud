import os
import json
from urllib.parse import quote
from typing import Union
from .mutable_local import set_mutable_local
from .store_file_local import _compute_file_hash
from .get_kachery_cloud_dir import get_kachery_cloud_dir


def link_file(filename: str, *, label: Union[str, None]=None):
    if not os.path.isabs(filename):
        filename = os.path.abspath(filename)

    # this will be efficient on subsequent calls because of lookup
    sha1 = _compute_file_hash(filename, algorithm='sha1')

    size0 = os.path.getsize(filename)
    kachery_cloud_dir = get_kachery_cloud_dir()
    s = sha1
    parent_dir = f'{kachery_cloud_dir}/linked_files/sha1/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}'
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    with open(f'{parent_dir}/{sha1}', 'w') as f:
        f.write(json.dumps({
            'path': filename,
            'size': size0,
            'mtime': os.stat(filename).st_mtime,
            'sha1': sha1
        }))

    uri = f'sha1://{sha1}'
    if label is not None:
        uri = f'{uri}?label={quote(label)}'
    return uri