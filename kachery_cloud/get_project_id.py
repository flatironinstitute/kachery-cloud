from .init import _get_client_info

def get_project_id():
    client_info = _get_client_info()
    if client_info is None:
        return None
    client = client_info['client']
    defaultProjectId = client.get('defaultProjectId', None)
    return defaultProjectId