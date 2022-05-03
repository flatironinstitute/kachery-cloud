from os import stat
from typing import Any, Callable, Union
from .._kacherycloud_request import _kacherycloud_request
from .upload_task_result import upload_task_result
from .._serialize import _serialize

def _run_task(*, task_type: str, task_name: str, task_job_id: str, task_function: Callable, task_input: Any, project_id: Union[str, None]):
    _set_task_status(task_name=task_name, task_job_id=task_job_id, status='started', project_id=project_id)
    try:
        result = task_function(**task_input)
        result = _serialize(result)
    except Exception as err:
        _set_task_status(task_name=task_name, task_job_id=task_job_id, status='error', error=str(err), project_id=project_id)
        return False
    if task_type == 'calculation':
        upload_task_result(task_name=task_name, task_job_id=task_job_id, task_result=result, project_id=project_id)
    _set_task_status(task_name=task_name, task_job_id=task_job_id, status='finished', project_id=project_id)
    return True

def _set_task_status(*, task_name: str, task_job_id: str, status: str, error: Union[str, None]=None, project_id: Union[str, None]):
    print(f'Task {status}: {task_name}')
    payload = {
        'type': 'publishToPubsubChannel',
        'channelName': 'provideTasks',
        'message': {
            'type': 'setTaskStatus',
            'taskName': task_name,
            'taskJobId': task_job_id,
            'status': status
        }
    }
    if error is not None:
        payload['message']['errorMessage'] = error
    if project_id is not None:
        payload['projectId'] = project_id
    _kacherycloud_request(payload)