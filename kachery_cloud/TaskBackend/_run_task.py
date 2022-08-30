from typing import Any, Callable, Union
import requests
import simplejson

from ..get_project_id import get_project_id
from .._kacherycloud_request import _kacherycloud_request
from .upload_task_result import upload_task_result
from .._serialize import _serialize

def _run_task(*, task_type: str, task_name: str, task_job_id: str, task_function: Callable, task_input: Any, project_id: str, extra_kwargs: dict):
    _set_task_status(task_name=task_name, task_job_id=task_job_id, status='started', project_id=project_id)
    try:
        result = task_function(**task_input, **extra_kwargs)
        serialized_result = _serialize(result)
    except Exception as err:
        _set_task_status(task_name=task_name, task_job_id=task_job_id, status='error', error=str(err), project_id=project_id)
        return False
    if task_type == 'calculation':
        upload_task_result(task_name=task_name, task_job_id=task_job_id, serialized_task_result=serialized_result, project_id=project_id)
    _set_task_status(task_name=task_name, task_job_id=task_job_id, status='finished', project_id=project_id)
    return True

def _set_task_status(*, task_name: str, task_job_id: str, status: str, error: Union[str, None]=None, project_id: str):
    if status == 'error':
        print(f'Error in task {task_name}: {error}')
    print(f'Task {status}: {task_name}')
    message = {
        'type': 'setTaskStatus',
        'taskName': task_name,
        'taskJobId': task_job_id,
        'status': status
    }
    if error is not None:
        message['errorMessage'] = error
    else:
        if status == 'error':
            raise Exception('Status is error, but no error string provided.')
    if not project_id.startswith('local:'):
        payload = {
            'type': 'publishToPubsubChannel',
            'channelName': 'provideTasks',
            'message': message
        }
        
        if project_id is not None:
            payload['projectId'] = project_id
        else:
            payload['projectId'] = get_project_id()
        _kacherycloud_request(payload)
    else:
        port = _get_port_from_project_id(project_id)
        _publish_local_pubsub_message(channel=f'provideTasks', message=message, port=port)

def _get_port_from_project_id(project_id: str):
    if not project_id.startswith('local:'):
        raise Exception(f'Unexpected project_id in _get_port_from_project_id(): {project_id}')
    a = project_id.split(':')
    if len(a) != 2:
        raise Exception(f'Unexpected project_id in _get_port_from_project_id(): {project_id}')
    return int(a[1])

def _publish_local_pubsub_message(*, channel: str, message: dict, port: int):
    req = {
        'type': 'publish',
        'channel': channel,
        'messageBody': simplejson.dumps(message)
    }
    resp = requests.post(f'http://localhost:{port}', json=req)
    if resp.status_code != 200:
        raise Exception(f'Error publishing pubsub message')
    response = resp.json()
    assert response['type'] == 'publish', 'Unexpected response in publish pubsub message'