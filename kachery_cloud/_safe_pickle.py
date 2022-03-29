from typing import Any
import pickle

def _safe_pickle(fname: str, x: Any):
    _check_safe_for_pickling(x)
    with open(fname, 'wb') as f:
        pickle.dump(x, f)

safe_builtins = {
    'range',
    'complex',
    'set',
    'frozenset',
    'slice',
}

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # carefully limit which classes may be loaded
        okay = False
        if module == "builtins" and name in safe_builtins:
            okay = True
        elif module == 'numpy':
            if name in ['ndarray', 'dtype']:
                okay = True
        elif module == 'numpy.core.multiarray':
            if name in ['_reconstruct', 'scalar']:
                okay = True
        if okay:
            return pickle.Unpickler.find_class(self, module, name)
        else:
            raise Exception(f'Not able to safe-unpickle {module}/{name}. If this is safe, consider whitelisting this module/name.')

def _safe_unpickle(fname: str):
    with open(fname, 'rb') as f:
        return RestrictedUnpickler(f).load()

def _check_safe_for_pickling(x: Any):
    if isinstance(x, int) or isinstance(x, float) or isinstance(x, str) or isinstance(x, bool) or (x is None):
        pass
    elif isinstance(x, range) or isinstance(x, complex) or isinstance(x, slice):
        # do not include "set" for now
        pass
    elif isinstance(x, dict):
        y = {}
        for k, v in x.items():
            _check_safe_for_pickling(v)
    elif isinstance(x, list):
        for a in x:
            _check_safe_for_pickling(a)
    elif isinstance(x, tuple):
        for a in x:
            _check_safe_for_pickling(a)
    elif _is_numpy_array(x):
        pass
    elif _is_numpy_number(x):
        pass
    elif _is_numpy_bool(x):
        pass
    else:
        raise Exception(f'Not safe for pickling: ({type(x)}). Perhaps this type should be whitelisted.')

def _is_numpy_array(x):
    try:
        import numpy as np
    except:
        return False
    return isinstance(x, np.ndarray)

def _is_numpy_number(x):
    try:
        import numpy as np
    except:
        return False
    return isinstance(x, np.integer) or isinstance(x, np.floating) or isinstance(x, np.complexfloating)

def _is_numpy_bool(x):
    try:
        import numpy as np
    except:
        return False
    return isinstance(x, np.bool) or isinstance(x, np.bool_)