from ._kacherycloud_request import _kacherycloud_request

_global_data = {
    'project_base_urls': {}
}

def _get_project_bucket_base_url(project_id: str):
    if project_id in _global_data['project_base_urls']:
        return _global_data['project_base_urls'][project_id]
    payload = {
        'type': 'getProjectBucketBaseUrl',
        'projectId': project_id
    }
    response = _kacherycloud_request(payload)
    found = response['found']
    if not found:
        raise Exception(f'Project not found: {project_id}')
    bucket_base_url = response['bucketBaseUrl']
    if not bucket_base_url:
        raise Exception('Unexpected, no bucket base url')
    _global_data['project_base_urls'][project_id] = bucket_base_url
    return bucket_base_url