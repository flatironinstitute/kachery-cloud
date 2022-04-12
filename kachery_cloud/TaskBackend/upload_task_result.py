from typing import Union
import requests
import simplejson
import time

from .._serialize import _serialize, _deserialize
from .._json_stringify_deterministic import _json_stringify_deterministic
from .._sha1_of_string import _sha1_of_string
from .._get_project_bucket_base_url import _get_project_bucket_base_url
from .._kacherycloud_request import _kacherycloud_request

def upload_task_result(*, task_name: str, task_job_id: dict, task_result: dict, project_id: Union[str, None]=None):
    task_result_serialized = _serialize(task_result)
    task_result_text = _json_stringify_deterministic(task_result_serialized)
    size = len(task_result_text)

    payload = {
        'type': 'initiateTaskResultUpload',
        'taskName': task_name,
        'taskJobId': task_job_id,
        'size': size
    }
    if project_id is not None:
        payload['projectId'] = project_id
    response = _kacherycloud_request(payload)
    signed_upload_url = response['signedUploadUrl']
    resp_upload = requests.put(signed_upload_url, data=task_result_text)
    if resp_upload.status_code != 200:
        raise Exception(f'Error uploading task_result to bucket ({resp_upload.status_code}) {resp_upload.reason}: {resp_upload.text}')
    payload2 = {
        'type': 'finalizeTaskResultUpload',
        'taskName': task_name,
        'taskJobId': task_job_id,
        'size': size
    }
    if project_id is not None:
        payload2['projectId'] = project_id
    response2 = _kacherycloud_request(payload2)

def download_task_result(*, task_name: str, task_job_id: dict, project_id: str):
    project_bucket_base_url = _get_project_bucket_base_url(project_id)
    s = task_job_id
    url = f'{project_bucket_base_url}/taskResults/{task_name}/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}/{s}'
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f'Error downloading task result ({resp.status_code}) {resp.reason}: {resp.text}')
    task_result = simplejson.loads(resp.content)
    task_result_deserialized = _deserialize(task_result)
    return task_result_deserialized