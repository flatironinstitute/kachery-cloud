from typing import Union
from .TaskBackend.TaskClient import TaskClient, TaskErrorException
from .load_file import load_file
from ._access_group_encrypt import _access_group_decrypt


def request_file_experimental(uri: str, *, project_id: str, dest: Union[None, str]=None):
    # important to encrypt first before requesting the file
    if uri.startswith('sha1-enc://'):
        uri = _access_group_decrypt(uri)
    
    fname = load_file(uri, dest=dest)
    if fname is not None:
        return fname
    task_client = TaskClient(project_id=project_id)
    try:
        task_client.request_task(
            task_type='action',
            task_name='kachery_store_shared_file.1',
            task_input={
                'uri': uri
            }
        )
    except TaskErrorException as err:
        print(f'Error requesting file: {err.error_message}')
        return None
    return load_file(uri, dest=dest)
