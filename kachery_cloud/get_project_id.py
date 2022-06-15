import os
from .init import _get_client_info

def get_project_id():
    project_id = os.getenv('KACHERY_CLOUD_PROJECT', '')
    if project_id:
        return project_id
    client_info = _get_client_info()
    if client_info is None:
        return None
    client = client_info['client']
    defaultProjectId = client.get('defaultProjectId', None)
    return defaultProjectId