from ._json_stringify_deterministic import _json_stringify_deterministic
from ._sha1_of_string import _sha1_of_string


def sha1_of_dict(x: dict):
    a = _json_stringify_deterministic(x)
    return _sha1_of_string(a)