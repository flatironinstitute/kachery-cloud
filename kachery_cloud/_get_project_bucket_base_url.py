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
    project_base_url = response['projectBaseUrl']
    if not project_base_url:
        raise Exception('Unexpected, no project base url')
    _global_data['project_base_urls'][project_id] = project_base_url
    return project_base_url