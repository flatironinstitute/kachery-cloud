import os
import shutil
import requests
from typing import Union
from urllib.parse import quote

from .get_kachery_cloud_dir import get_kachery_cloud_dir

from ._kacherycloud_request import _kacherycloud_request
from .get_project_id import get_project_id
from .load_file import _random_string
from ._fs_operations import _makedirs, _chmod_file
from .store_file_local import _compute_file_hash

def store_file(filename: str, *, label: Union[str, None]=None, cache_locally: bool=False):
    size = os.path.getsize(filename)
    alg = 'sha1'
    hash0 = _compute_file_hash(filename, algorithm=alg)
    uri = f'{alg}://{hash0}'
    payload = {
        'type': 'initiateFileUpload',
        'size': size,
        'hashAlg': alg,
        'hash': hash0,
        'projectId': get_project_id()
    }
    response = _kacherycloud_request(payload)
    already_exists = response['alreadyExists']
    if already_exists:
        if label is not None:
            uri = f'{uri}?label={quote(label)}'
        return uri
    signed_upload_url = response['signedUploadUrl']
    object_key = response['objectKey']
    with open(filename, 'rb') as f:
        resp_upload = requests.put(signed_upload_url, data=f)
        if resp_upload.status_code != 200:
            raise Exception(f'Error uploading file to bucket ({resp_upload.status_code}) {resp_upload.reason}: {resp_upload.text}')
    payload2 = {
        'type': 'finalizeFileUpload',
        'objectKey': object_key,
        'hashAlg': alg,
        'hash': hash0,
        'projectId': get_project_id()
    }
    response2 = _kacherycloud_request(payload2)

    if cache_locally:
        kachery_cloud_dir = get_kachery_cloud_dir()
        e = hash0
        cache_parent_dir = f'{kachery_cloud_dir}/hash0/{e[0]}{e[1]}/{e[2]}{e[3]}/{e[4]}{e[5]}'
        if not os.path.exists(cache_parent_dir):
            _makedirs(cache_parent_dir)
        cache_filename = f'{cache_parent_dir}/{hash0}'
        if not os.path.exists(cache_filename):
            tmp_filename = f'{cache_filename}.tmp.{_random_string(8)}'
            shutil.copyfile(filename, tmp_filename)
            try:
                os.rename(tmp_filename, filename)
                _chmod_file(filename)
            except:
                if not os.path.exists(cache_filename):
                    raise Exception(f'Problem renaming file: {tmp_filename} {filename}')

    if label is not None:
        uri = f'{uri}?label={quote(label)}'
    return uri