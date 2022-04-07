import os
from typing import Union
import requests
from datetime import datetime
import simplejson

from .get_client_id import get_client_id
from ._client_keys import _sign_message_as_client
from ._kachery_cloud_api_url import _kachery_cloud_api_url
from ._serialize import _serialize, _deserialize
from ._json_stringify_deterministic import _json_stringify_deterministic
from ._sha1_of_string import _sha1_of_string
from ._get_project_bucket_base_url import _get_project_bucket_base_url

def upload_task_result(*, task_type: str, task_input: dict, task_result: dict, project_id: Union[str, None]=None):
    client_id = get_client_id()
    url = f'{_kachery_cloud_api_url}/api/kacherycloud'
    timestamp = int(datetime.timestamp(datetime.now()) * 1000)

    task_result_serialized = _serialize(task_result)
    task_result_text = _json_stringify_deterministic(task_result_serialized)
    size = len(task_result_text)
    task_input_hash = _sha1_of_string(_json_stringify_deterministic(task_input))

    payload = {
        'type': 'initiateTaskResultUpload',
        'timestamp': timestamp,
        'taskType': task_type,
        'taskInputHash': task_input_hash,
        'size': size
    }
    if project_id is not None:
        payload['projectId'] = project_id
    req = {
        'payload': payload,
        'fromClientId': client_id,
        'signature': _sign_message_as_client(payload)
    }
    resp = requests.post(url, json=req)
    if resp.status_code != 200:
        raise Exception(f'Error initiating task result upload ({resp.status_code}) {resp.reason}: {resp.text}')
    response = resp.json()
    signed_upload_url = response['signedUploadUrl']
    resp_upload = requests.put(signed_upload_url, data=task_result_text)
    if resp_upload.status_code != 200:
        raise Exception(f'Error uploading task_result to bucket ({resp_upload.status_code}) {resp_upload.reason}: {resp_upload.text}')
    payload2 = {
        'type': 'finalizeTaskResultUpload',
        'timestamp': timestamp,
        'taskType': task_type,
        'taskInputHash': task_input_hash,
        'size': size
    }
    req2 = {
        'payload': payload2,
        'fromClientId': client_id,
        'signature': _sign_message_as_client(payload2)
    }
    resp2 = requests.post(url, json=req2)
    if resp2.status_code != 200:
        raise Exception(f'Error finalizing task result upload ({resp2.status_code}) {resp2.reason}: {resp2.text}')
    response2 = resp2.json()

def download_task_result(*, task_type: str, task_input: dict, project_id: str):
    project_bucket_base_url = _get_project_bucket_base_url(project_id)
    task_input_hash = _sha1_of_string(_json_stringify_deterministic(task_input))
    s = task_input_hash
    url = f'{project_bucket_base_url}/taskResults/{task_type}/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}/{s}'
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f'Error downloading task result ({resp.status_code}) {resp.reason}: {resp.text}')
    task_result = simplejson.loads(resp.content)
    task_result_deserialized = _deserialize(task_result)
    return task_result_deserialized