import os
import json
from urllib.parse import quote
from typing import Union
from .mutable_local import set_mutable_local
from .store_file_local import _compute_file_hash


def link_file(filename: str, *, label: Union[str, None]=None):
    if not os.path.isabs(filename):
        filename = os.path.abspath(filename)

    # this will be efficient on subsequent calls because of lookup
    sha1 = _compute_file_hash(filename, algorithm='sha1')

    size0 = os.path.getsize(filename)
    set_mutable_local(f'@linked_files/@sha1/{sha1}', json.dumps({
        'path': filename,
        'size': size0,
        'mtime': os.stat(filename).st_mtime,
        'sha1': sha1
    }))

    uri = f'sha1://{sha1}'
    if label is not None:
        uri = f'{uri}?label={quote(label)}'
    return uri