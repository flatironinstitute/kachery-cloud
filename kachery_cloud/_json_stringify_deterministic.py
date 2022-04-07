from typing import Any
from numpy import floor
import simplejson


def _json_stringify_deterministic(x: Any):
    separators=(',', ':')
    x = _replace_float_by_int_when_appropriate(x)
    return simplejson.dumps(x, separators=separators, indent=None, allow_nan=False, sort_keys=True)

def _replace_float_by_int_when_appropriate(x):
    if isinstance(x, float):
        if x == floor(x):
            return int(x)
    elif isinstance(x, dict):
        ret = {}
        for k in x.keys():
            ret[k] = _replace_float_by_int_when_appropriate(x[k])
        return ret
    elif isinstance(x, tuple):
        return tuple([_replace_float_by_int_when_appropriate(a) for a in x])
    elif isinstance(x, list):
        return [_replace_float_by_int_when_appropriate(a) for a in x]
    else:
        return x