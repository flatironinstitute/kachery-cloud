import os
import socket
import urllib.parse
import logging

from kachery_cloud.get_kachery_cloud_dir import get_kachery_cloud_dir

from .get_client_id import get_client_id
from ._client_keys import _sign_message_as_client
from ._get_kachery_gateway_url import _get_kachery_gateway_url
from ._kachery_gateway_request import _kachery_gateway_request
from ._get_local_client_config import _get_local_client_config


_global_init = {
    'client_info': 0 # 0 means we have not yet queried. None means not found.
}

def get_client_info():
    """
    Returns kachery cloud client info.
    If the client is not registered, returns None.

    Returns
    -------
    response: dict
        The response dict from the Kachery Gateway
    """
    # first check if we are using a custom storage backend
    from ._custom_storage_backend import get_custom_storage_backend
    sb = get_custom_storage_backend()
    if sb is not None and hasattr(sb, 'store_file'):
        return {
            'type': 'getClientInfo',
            'found': True,
            'client': 'custom_storage_backend'
        }

    if _global_init['client_info'] != 0:
        if _global_init['client_info']["client"]["clientId"] != get_client_id():
            logging.warning("Client ID in current `KACHERY_CLOUD_DIR`, does not match cached client info. \n"
                            + "If experiencing issues, please restart your python session and register the client again "
                            + f"with `KACHERY_CLOUD_DIR` set to {os.getenv('KACHERY_CLOUD_DIR')}")
        return _global_init['client_info']
    client_id = get_client_id()
    kachery_zone = os.environ.get('KACHERY_ZONE', 'default')
    payload = {
        'type': 'getClientInfo',
        'clientId': client_id,
        'zone': kachery_zone
    }
    response = _kachery_gateway_request(payload)
    # response = _kacherycloud_request(payload)
    found = response['found']
    if found:
        _global_init['client_info'] = response
        return response
    else:
        return None

def init():
    client_info = get_client_info()
    if client_info is None:
        client_id = get_client_id()
        signature = _sign_message_as_client({
            'type': 'addClient'
        })
        label = socket.gethostname()
        kachery_zone = os.environ.get('KACHERY_ZONE', 'default')
        url = f'{_get_kachery_gateway_url()}/registerClient/{client_id}?signature={signature}&zone={kachery_zone}&label={urllib.parse.quote(label)}'
        print('')
        print(url)
        print('')
        print('Click the above link to register this kachery cloud client. After pressing the "REGISTER CLIENT" button on the website, press [Enter] in this terminal to continue.')
        print('')
        input()
        print('Checking...')
        client_info = get_client_info()
        if client_info is None:
            raise Exception('Failed to initialize this kachery client')
        print(f'Client initialized successfully.')
    else:
        client_id = get_client_id()
        print('This client has already been registered.')
        print('Click the following link to configure the client:')
        url = f'{_get_kachery_gateway_url()}/client/{client_id}'
        print(url)
        print('')
    client = client_info['client']
    label = client['label']
    client_owner = client['ownerId']
    print(f'Client ID: {client_id}')
    print(f'Label: {label}')
    print(f'Owner: {client_owner}')

    print('')
    print('* Kachery-cloud is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.')