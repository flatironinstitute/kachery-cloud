import os
from typing import Union
import requests
import simplejson
import kachery_cloud as kcl

from ..get_project_id import get_project_id
from .._serialize import _deserialize
from .._json_stringify_deterministic import _json_stringify_deterministic
from .._get_project_bucket_base_url import _get_project_bucket_base_url
from .._kacherycloud_request import _kacherycloud_request

def upload_task_result(*, task_name: str, task_job_id: dict, serialized_task_result: dict, project_id: Union[str, None]=None):
    if project_id is None:
        project_id = get_project_id()
    task_result_text = _json_stringify_deterministic(serialized_task_result)
    size = len(task_result_text)

    if not project_id.startswith('local:'):
        payload = {
            'type': 'initiateTaskResultUpload',
            'taskName': task_name,
            'taskJobId': task_job_id,
            'size': size
        }
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
        payload2['projectId'] = project_id
        response2 = _kacherycloud_request(payload2)
    else:
        _store_task_result_text_locally(task_name=task_name, task_job_id=task_job_id, task_result_text=task_result_text)

def download_task_result(*, task_name: str, task_job_id: dict, project_id: str):
    if not project_id.startswith('local:'):
        project_bucket_base_url = _get_project_bucket_base_url(project_id)
        s = task_job_id
        url = f'{project_bucket_base_url}/taskResults/{task_name}/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}/{s}'
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception(f'Error downloading task result ({resp.status_code}) {resp.reason}: {resp.text}')
        task_result_text = resp.content
    else:
        task_result_text = _load_task_result_text_locally(task_name=task_name, task_job_id=task_job_id)
    simplejson.loads(task_result_text)
    task_result_deserialized = _deserialize(task_result_text)
    return task_result_deserialized

def _store_task_result_text_locally(*, task_name: str, task_job_id: str, task_result_text: str):
    kcdir = kcl.get_kachery_cloud_dir()
    s = task_job_id
    parentdir = f'{kcdir}/task_results/{task_name}/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}'
    if not os.path.exists(parentdir):
        os.makedirs(parentdir)
    fname = f'{parentdir}/{s}'
    with open(fname, 'w') as f:
        f.write(task_result_text)

def _load_task_result_text_locally(*, task_name: str, task_job_id: str):
    kcdir = kcl.get_kachery_cloud_dir()
    s = task_job_id
    parentdir = f'{kcdir}/task_results/{task_name}/{s[0]}{s[1]}/{s[2]}{s[3]}/{s[4]}{s[5]}'
    fname = f'{parentdir}/{s}'
    with open(fname, 'r') as f:
        return f.read()