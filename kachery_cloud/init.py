from datetime import datetime
from click import prompt
import requests
import socket
import urllib.parse

from .get_client_id import get_client_id
from ._client_keys import _sign_message_as_client
from ._kachery_cloud_api_url import _kachery_cloud_api_url


_global_init = {
    'client_info': 0 # 0 means we have not yet queried. None means not found.
}

def _get_client_info():
    if _global_init['client_info'] != 0:
        return _global_init['client_info']
    client_id = get_client_id()
    timestamp = int(datetime.timestamp(datetime.now()) * 1000)
    payload = {
        'type': 'getClientInfo',
        'timestamp': timestamp,
        'clientId': client_id
    }
    req = {
        'payload': payload,
        'fromClientId': client_id,
        'signature': _sign_message_as_client(payload)
    }
    url = f'{_kachery_cloud_api_url}/api/kacherycloud'
    resp = requests.post(url, json=req)
    if resp.status_code != 200:
        raise Exception(f'Error getting client info ({resp.status_code}) {resp.reason}: {resp.text}')
    response = resp.json()
    found = response['found']
    if found:
        _global_init['client_info'] = response
        return response
    else:
        return None

def init():
    client_info = _get_client_info()
    if client_info is None:
        client_id = get_client_id()
        signature = _sign_message_as_client({
            'type': 'addClient'
        })
        label = socket.gethostname()
        url = f'{_kachery_cloud_api_url}/registerClient/{client_id}?signature={signature}&label={urllib.parse.quote(label)}'
        print('')
        print(url)
        print('')
        print('Click the above link to register this kachery cloud client. Then press [Enter] to continue.')
        print('')
        input()
        print('Checking...')
        client_info = _get_client_info()
        if client_info is None:
            raise Exception('Failed to initialize this kachery client')
        print(f'Client initialized successfully.')
    else:
        print('This client has already been registered.')
    client = client_info['client']
    label = client['label']
    default_project_id = client.get('defaultProjectId', None)
    client_owner = client['ownerId']
    print(f'Label: {label}')
    print(f'Owner: {client_owner}')
    print(f'Default project ID: {default_project_id}')