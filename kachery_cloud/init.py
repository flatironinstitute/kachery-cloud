import socket
import urllib.parse

from .get_client_id import get_client_id
from ._client_keys import _sign_message_as_client
from ._kachery_cloud_api_url import _kachery_cloud_api_url
from ._kacherycloud_request import _kacherycloud_request


_global_init = {
    'client_info': 0 # 0 means we have not yet queried. None means not found.
}

def _get_client_info():
    if _global_init['client_info'] != 0:
        return _global_init['client_info']
    client_id = get_client_id()
    payload = {
        'type': 'getClientInfo',
        'clientId': client_id
    }
    response = _kacherycloud_request(payload)
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
        print('Click the above link to register this kachery cloud client. After pressing the "Yes, proceed" button on the website, press [Enter] in this terminal to continue.')
        print('')
        input()
        print('Checking...')
        client_info = _get_client_info()
        if client_info is None:
            raise Exception('Failed to initialize this kachery client')
        print(f'Client initialized successfully.')
    else:
        client_id = get_client_id()
        print('This client has already been registered.')
        print('Click the following link to configure the client:')
        print('')
        url = f'{_kachery_cloud_api_url}/client/{client_id}'
        print(url)
        print('')
    client = client_info['client']
    label = client['label']
    default_project_id = client.get('defaultProjectId', None)
    client_owner = client['ownerId']
    print(f'Client ID: {client_id}')
    print(f'Label: {label}')
    print(f'Owner: {client_owner}')
    print(f'Default project ID: {default_project_id}')