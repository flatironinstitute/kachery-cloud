from typing import Union
from ._kacherycloud_request import _kacherycloud_request


def set_mutable(key: str, value: str, *, project_id: Union[str, None]=None):
    if len(value) > 1000:
        raise Exception('Value too large for mutable')
    payload = {
        'type': 'setMutable',
        'mutableKey': key,
        'value': value
    }
    if project_id is not None:
        payload['projectId'] = project_id
    response = _kacherycloud_request(payload)

def get_mutable(key: str, *, project_id: Union[str, None]=None):
    payload = {
        'type': 'getMutable',
        'mutableKey': key
    }
    if project_id is not None:
        payload['projectId'] = project_id
    response = _kacherycloud_request(payload)
    if not response['found']:
        return None
    return response['value']