import requests
from datetime import datetime
from .get_client_id import get_client_id
from ._client_keys import _sign_message_as_client
from ._kachery_cloud_api_url import _kachery_cloud_api_url

_global_data = {
    'project_base_urls': {}
}

def _get_project_bucket_base_url(project_id: str):
    client_id = get_client_id()
    if project_id in _global_data['project_base_urls']:
        return _global_data['project_base_urls'][project_id]
    timestamp = int(datetime.timestamp(datetime.now()) * 1000)
    payload = {
        'type': 'getProjectBucketBaseUrl',
        'timestamp': timestamp,
        'projectId': project_id
    }
    req = {
        'payload': payload,
        'fromClientId': client_id,
        'signature': _sign_message_as_client(payload)
    }
    url = f'{_kachery_cloud_api_url}/api/kacherycloud'
    resp = requests.post(url, json=req)
    if resp.status_code != 200:
        raise Exception(f'Error requesting project bucket base url ({resp.status_code}) {resp.reason}: {resp.text}')
    response = resp.json()
    found = response['found']
    if not found:
        raise Exception(f'Project not found: {project_id}')
    bucket_base_url = response['bucketBaseUrl']
    if not bucket_base_url:
        raise Exception('Unexpected, no bucket base url')
    _global_data['project_base_urls'][project_id] = bucket_base_url
    return bucket_base_url