import os
import requests
from typing import Union

from ._kachery_cloud_api_url import _kachery_cloud_api_url
from ._kacherycloud_request import _kacherycloud_request

def store_file(filename: str, *, label: Union[str, None]=None):
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
        uri = f'ipfs://{cid}'
    elif _kachery_cloud_api_url:
        size = os.path.getsize(filename)
        payload = {
            'type': 'initiateIpfsUpload',
            'size': size
        }
        response = _kacherycloud_request(payload)
        signed_upload_url = response['signedUploadUrl']
        object_key = response['objectKey']
        with open(filename, 'rb') as f:
            resp_upload = requests.put(signed_upload_url, data=f)
            if resp_upload.status_code != 200:
                raise Exception(f'Error uploading file to bucket ({resp_upload.status_code}) {resp_upload.reason}: {resp_upload.text}')
        payload2 = {
            'type': 'finalizeIpfsUpload',
            'objectKey': object_key
        }
        response2 = _kacherycloud_request(payload2)
        cid = response2['cid']
        uri = f'ipfs://{cid}'
    else:
        raise Exception('Unexpected: no method found for uploading file')
    if label is not None:
        uri = f'{uri}?label={label}'
    return uri