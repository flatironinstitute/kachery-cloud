from typing import Any, Union

from .store_file import store_file
from .load_file import load_file
from .TemporaryDirectory import TemporaryDirectory
from ._safe_pickle import _safe_pickle, _safe_unpickle
    
def store_text(text: str, label: Union[str, None]=None) -> str:
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/file.dat'
        with open(fname, 'w') as f:
            f.write(text)
        return store_file(fname, label=label)

def store_json(x: Any, *, separators=(',', ':'), indent=None, label: Union[str, None]=None) -> str:
    import simplejson
    text = simplejson.dumps(x, separators=separators, indent=indent, allow_nan=False)
    return store_text(text, label=label)

def store_npy(array: Any, label: Union[str, None]=None) -> str:
    import numpy as np
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/file.npy'
        np.save(fname, array, allow_pickle=False)
        return store_file(fname, label=label)

def store_pkl(x: Any, label: Union[str, None]=None) -> str:
    with TemporaryDirectory() as tmpdir:
        fname = f'{tmpdir}/file.npy'
        _safe_pickle(fname, x)
        return store_file(fname, label=label)

def load_text(uri: str) -> Union[str, None]:
    local_path = load_file(uri)
    if local_path is None:
        return None
    with open(local_path, 'r') as f:
        return f.read()

def load_json(uri: str) -> Union[dict, None]:
    import simplejson
    local_path = load_file(uri)
    if local_path is None:
        return None
    with open(local_path, 'r') as f:
        return simplejson.load(f)

def load_npy(uri: str) -> Union[Any, None]:
    import numpy as np
    local_path = load_file(uri)
    if local_path is None:
        return None
    return np.load(local_path, allow_pickle=False)

def load_pkl(uri: str) -> Union[Any, None]:
    local_path = load_file(uri)
    if local_path is None:
        return None
    return _safe_unpickle(local_path)