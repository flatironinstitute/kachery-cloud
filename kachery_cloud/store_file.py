import os
import requests

from .get_client_id import get_client_id
from ._client_keys import _sign_message_as_client
from ._kachery_cloud_api_url import _kachery_cloud_api_url

def store_file(filename: str):
    # web3_storage_token = os.environ.get('HASHIO_WEB3_STORAGE_TOKEN', None)
    web3_storage_token = None
    # if not web3_storage_token and not hashio_api_url:
    #     raise Exception(f'Environment variable not set: HASHIO_WEB3_STORAGE_TOKEN or HASHIO_API_URL. See the hashio docs.')
    if web3_storage_token:
        url = 'https://api.web3.storage/upload'
        headers = {
            'Authorization': f'Bearer {web3_storage_token}'
        }
        with open(filename, 'rb') as f:
            resp = requests.post(url, data=f, headers=headers)
        if resp.status_code != 200:
            raise Exception(f'Error storing file ({resp.status_code}) {resp.reason}: {resp.text}')
        cid = resp.json()['cid']
        return f'ipfs://{cid}'
    elif _kachery_cloud_api_url:
        client_id = get_client_id()
        signature = _sign_message_as_client({'type': 'uploadToIpfs'})
        with open(filename, 'rb') as f:
            url = f'{_kachery_cloud_api_url}/api/uploadToIpfs'
            headers = {
                'kachery-cloud-client-id': client_id,
                'kachery-cloud-client-signature': signature
            }
            resp = requests.post(url, data=f, headers=headers)
        if resp.status_code != 200:
            raise Exception(f'Error storing file ({resp.status_code}) {resp.reason}: {resp.text}')
        cid = resp.json()['cid']
        return f'ipfs://{cid}'
    else:
        raise Exception('Unexpected: no method found for uploading file')