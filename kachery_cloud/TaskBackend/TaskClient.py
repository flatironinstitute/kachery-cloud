from typing import Any, Union, Protocol
import random
import math
import time

from .LocalPubsubListener import LocalPubsubListener

from ..get_project_id import get_project_id
from .upload_task_result import download_task_result
from .PubsubListener import PubsubListener
from .._kacherycloud_request import _kacherycloud_request
from ..get_client_id import get_client_id
from .._json_stringify_deterministic import _json_stringify_deterministic
from .._sha1_of_string import _sha1_of_string

class TaskRequestCallback(Protocol):
    def __call__(self, *, task_type: str, task_name: str, task_input: dict, task_job_id: str): ...

class TaskErrorException(Exception):
    def __init__(self, message: str) -> None:
        self.error_message = message
        super().__init__(message)

class TaskClient:
    def __init__(self, *, project_id: Union[None, str]=None, backend_id: Union[str, None]=None) -> None:
        if project_id is None:
            project_id = get_project_id()
        self._project_id = project_id
        self._backend_id = backend_id
    def request_task(self, *, task_type: str, task_name: str, task_input: dict):
        status: Union[str, None] = None
        result: Union[Any, None] = None
        error: Union[str, None] = None

        def handle_message(*, channel: str, message: dict):
            nonlocal status
            nonlocal error
            nonlocal result
            if message['type'] == 'setTaskStatus':
                if message['taskName'] == task_name:
                    if message['taskJobId'] == task_job_id:
                        status = message['status']
                        if status == 'error':
                            error = message['errorMessage']
                        elif status == 'finished':
                            if task_type == 'calculation':
                                result = download_task_result(task_name=task_name, task_job_id=task_job_id, project_id=self._project_id)
        
        if task_type == 'calculation':
            task_job_id = _sha1_of_string(_json_stringify_deterministic({
                'taskName': task_name,
                'taskInput': task_input
            }))
        else:
            task_job_id = _sha1_of_string(_random_string(100))
        
        if task_type == 'calculation':
            try:
                result = download_task_result(task_name=task_name, task_job_id=task_job_id, project_id=self._project_id)
            except:
                result = None
            if result is not None:
                return result
        
        request_task_message = {
            'type': 'requestTask',
            'taskType': task_type,
            'taskName': task_name,
            'taskInput': task_input,
            'taskJobId': task_job_id
        }
        if self._backend_id is not None:
            request_task_message['backendId'] = self._backend_id
        if not self._project_id.startswith('local:'):
            client_id = get_client_id()

            # subscribe to the provideTasks channel
            # to get notified when a task status has changed
            payload_sub = {
                'type': 'subscribeToPubsubChannel',
                'channelName': 'provideTasks'
            }
            payload_sub['projectId'] = self._project_id
            response_sub = _kacherycloud_request(payload_sub)
            subscribe_key = response_sub['subscribeKey']
            subscribe_token = response_sub['token']
            pubsub_channel_name = response_sub['pubsubChannelName']

            def renew_access_token():
                raise Exception('not used')
            listener = PubsubListener(
                channels=[pubsub_channel_name],
                uuid=client_id,
                subscribe_key=subscribe_key,
                access_token=subscribe_token,
                renew_access_token_callback=renew_access_token
            )
            listener.on_message(handle_message)
            listener.start()
            
            # request a task on the requestTasks pubsub channel
            payload = {
                'type': 'publishToPubsubChannel',
                'channelName': 'requestTasks',
                'message': request_task_message
            }
            if self._project_id is not None:
                payload['projectId'] = self._project_id
            else:
                payload['projectId'] = get_project_id()
            _kacherycloud_request(payload)
        else:
            from ._run_task import _get_port_from_project_id, _publish_local_pubsub_message
            port = _get_port_from_project_id(self._project_id)
            listener = LocalPubsubListener(channel=f'provideTasks', port=port)
            listener.on_message(handle_message)
            listener.start()
            _publish_local_pubsub_message(channel=f'requestTasks', message=request_task_message, port=port)

        announced_started = False
        try:
            while True:
                listener.wait(0.1)
                if status == 'finished':
                    return result
                elif status == 'error':
                    raise TaskErrorException(error)
                elif status == 'started':
                    if not announced_started:
                        print('Task started')
                        announced_started = True
        finally:
            listener.stop()

    def listen_for_task_requests(self, callback: TaskRequestCallback):
        def handle_message(*, channel: str, message: dict):
            if message['type'] == 'requestTask':
                task_type = message['taskType']
                task_name = message['taskName']
                task_input = message['taskInput']
                task_job_id = message['taskJobId']
                backend_id = message.get('backendId', None)
                if task_type == 'calculation':
                    check_task_job_id = _sha1_of_string(_json_stringify_deterministic({
                        'taskName': task_name,
                        'taskInput': task_input
                    }))
                    if check_task_job_id != task_job_id:
                        raise Exception('Mismatch between task job ID and computed task job ID')
                callback(task_type=task_type, task_name=task_name, task_input=task_input, task_job_id=task_job_id, backend_id=backend_id)
        if not self._project_id.startswith('local:'):
            def subscribe_to_request_tasks_channel():
                # subscribe to the requestTasks channel
                # to listen for incoming tasks
                payload = {
                    'type': 'subscribeToPubsubChannel',
                    'channelName': 'requestTasks'
                }
                if self._project_id is not None:
                    payload['projectId'] = self._project_id
                else:
                    payload['projectId'] = get_project_id()
                return _kacherycloud_request(payload)
            def renew_access_token():
                while True:
                    try:
                        r = subscribe_to_request_tasks_channel()
                        break
                    except Exception as e:
                        print(e)
                        print('Problem renewing access token. Will retry in 30 seconds...')
                        time.sleep(30)
                return r['token']
                    
            client_id = get_client_id()
            response = subscribe_to_request_tasks_channel()
            listener = PubsubListener(
                channels=[response['pubsubChannelName']],
                uuid=client_id,
                subscribe_key=response['subscribeKey'],
                access_token=response['token'],
                renew_access_token_callback=renew_access_token
            )
            listener.on_message(handle_message)
            listener.start()
            return listener
        else:
            from ._run_task import _get_port_from_project_id
            port = _get_port_from_project_id(self._project_id)
            listener = LocalPubsubListener(channel=f'requestTasks', port=port)
            listener.on_message(handle_message)
            listener.start()
            return listener

def _random_string(num_chars: int) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(num_chars))