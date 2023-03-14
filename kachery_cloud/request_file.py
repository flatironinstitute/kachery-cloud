from typing import Union
from dataclasses import dataclass
import os
import requests
from .load_file import load_file_info, load_file_local
from ._kachery_gateway_request import _kachery_gateway_request

@dataclass
class RequestFileResult:
    found: Union[None, bool] = None
    queued: Union[None, bool] = None
    completed: Union[None, bool] = None
    running: Union[None, bool] = None
    local: bool = False
    errored: bool = False
    error_message: str = ''
    size: Union[None, int] = None
    bytes_uploaded: Union[None, int] = None

def request_file(uri: str, *, timeout_sec: float, ignore_local: bool=False, ignore_bucket: bool=False, resource_url: Union[str, None]=None) -> RequestFileResult:
    if resource_url is None:
        resource_url = os.getenv('KACHERY_RESOURCE_URL', None)
        if resource_url is None:
            raise Exception('In request_file: environment variable not set: KACHERY_RESOURCE_URL')
    if not ignore_local:
        a0 = load_file_local(uri)
        if a0 is not None:
            return RequestFileResult(
                found=True,
                size=os.path.getsize(a0),
                local=True
            )
    if not ignore_bucket:
        x0 = load_file_info(uri)
        if (x0 is not None) and (x0['found']):
            return RequestFileResult(
                found=True,
                size=x0['size'],
                completed=True
            )
    resource_name = resource_url.split('/')[-1]
    req = {
        'type': 'requestFromClient',
        'resourceName': resource_name,
        'zone': os.getenv('KACHERY_ZONE', 'default'),
        'request': {
            'type': 'fileUpload',
            'uri': _remove_query_string_from_uri(uri),
            'timeoutMsec': timeout_sec * 1000
        },
        'timeoutMsec': (timeout_sec + 5) * 1000 # add a few seconds to account for the overhead (not ideal system)
    }
    resp = requests.post(resource_url, json=req)
    if resp.status_code != 200:
        raise Exception(f'Error in requestFromClient: ({resp.status_code}) {resp.reason}: {resp.text}')
    response = resp.json()
    if response['type'] != 'responseToClient':
        raise Exception('Unexpected response to requestFromClient')
    if response.get('error', ''):
        raise Exception(f'Error requesting file: {response["error"]}')
    rr = response['response']
    if rr['type'] != 'fileUpload':
        raise Exception('Unexpected fileUpload response')
    status = rr['status']
    status_str = status['status'] # 'not-found' | 'queued' | 'running' | 'completed' | 'error'
    size = status.get('size', None)
    bytes_uploaded = status.get('bytesUploaded', None)
    error_str = status.get('error', '')
    return RequestFileResult(
        found = status_str in ['queued', 'running', 'completed'],
        queued = status_str == 'queued',
        completed = status_str == 'completed',
        running = status_str == 'running',
        errored = status_str == 'error',
        error_message = error_str,
        size = size,
        bytes_uploaded = bytes_uploaded
    )

def _remove_query_string_from_uri(uri: str):
    i = uri.find('?')
    if i < 0: return uri
    return uri[:i]