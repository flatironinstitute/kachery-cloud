import os
import requests
from datetime import datetime

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
        url = f'{_kachery_cloud_api_url}/api/kacherycloud'
        timestamp = int(datetime.timestamp(datetime.now()) * 1000)
        size = os.path.getsize(filename)
        payload = {
            'type': 'initiateIpfsUpload',
            'timestamp': timestamp,
            'size': size
        }
        req = {
            'payload': payload,
            'fromClientId': client_id,
            'signature': _sign_message_as_client(payload)
        }
        resp = requests.post(url, json=req)
        if resp.status_code != 200:
            raise Exception(f'Error initiating ipfs upload ({resp.status_code}) {resp.reason}: {resp.text}')
        response = resp.json()
        signed_upload_url = response['signedUploadUrl']
        object_key = response['objectKey']
        with open(filename, 'rb') as f:
            resp_upload = requests.put(signed_upload_url, data=f)
            if resp_upload.status_code != 200:
                raise Exception(f'Error uploading file to bucket ({resp_upload.status_code}) {resp_upload.reason}: {resp_upload.text}')
        payload2 = {
            'type': 'finalizeIpfsUpload',
            'timestamp': timestamp,
            'objectKey': object_key
        }
        req2 = {
            'payload': payload2,
            'fromClientId': client_id,
            'signature': _sign_message_as_client(payload2)
        }
        resp2 = requests.post(url, json=req2)
        if resp2.status_code != 200:
            raise Exception(f'Error finalizing ipfs upload ({resp2.status_code}) {resp2.reason}: {resp2.text}')
        response2 = resp2.json()
        cid = response2['cid']
        return f'ipfs://{cid}'
    else:
        raise Exception('Unexpected: no method found for uploading file')