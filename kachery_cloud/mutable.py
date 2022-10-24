from typing import Union

from .get_project_id import get_project_id
from ._kacherycloud_request import _kacherycloud_request


def set_mutable(key: str, value: str, *, project_id: Union[str, None]=None):
    if len(value) > 100000:
        raise Exception('Value too large for mutable')
    payload = {
        'type': 'setMutable',
        'mutableKey': key,
        'value': value
    }
    if project_id is not None:
        payload['projectId'] = project_id
    else:
        project_id = get_project_id()
        if project_id:
            payload['projectId'] = get_project_id()
    response = _kacherycloud_request(payload)

def get_mutable(key: str, *, project_id: Union[str, None]=None):
    payload = {
        'type': 'getMutable',
        'mutableKey': key
    }
    if project_id is not None:
        payload['projectId'] = project_id
    else:
        payload['projectId'] = get_project_id()
    response = _kacherycloud_request(payload)
    if not response['found']:
        return None
    return response['value']

def delete_mutable(key: str, *, project_id: Union[str, None]=None):
    payload = {
        'type': 'deleteMutable',
        'mutableKey': key,
        'isFolder': False
    }
    if project_id is not None:
        payload['projectId'] = project_id
    else:
        payload['projectId'] = get_project_id()
    response = _kacherycloud_request(payload)

def delete_mutable_folder(key: str, *, project_id: Union[str, None]=None):
    payload = {
        'type': 'deleteMutable',
        'mutableKey': key,
        'isFolder': True
    }
    if project_id is not None:
        payload['projectId'] = project_id
    else:
        payload['projectId'] = get_project_id()
    response = _kacherycloud_request(payload)