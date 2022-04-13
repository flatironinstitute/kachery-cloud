from typing import Any, Union, Protocol
import random
import time

from .upload_task_result import upload_task_result, download_task_result
from .PubsubListener import PubsubListener
from .._kacherycloud_request import _kacherycloud_request
from ..get_client_id import get_client_id
from .._json_stringify_deterministic import _json_stringify_deterministic
from .._sha1_of_string import _sha1_of_string

class TaskRequestCallback(Protocol):
    def __call__(self, *, task_type: str, task_name: str, task_input: dict, task_job_id: str): ...

class TaskClient:
    def __init__(self, *, project_id: Union[None, str]=None) -> None:
        self._project_id = project_id
    def download_task_result(self, *, task_name: str, task_job_id: str):
        return download_task_result(task_name=task_name, task_job_id=task_job_id)
    def request_task(self, *, task_type: str, task_name: str, task_input: dict):
        client_id = get_client_id()

        payload_sub = {
            'type': 'subscribeToPubsubChannel',
            'channelName': 'provideTasks'
        }
        if self._project_id is not None:
            payload_sub['projectId'] = self._project_id
        response_sub = _kacherycloud_request(payload_sub)
        subscribe_key = response_sub['subscribeKey']
        subscribe_token = response_sub['token']
        pubsub_channel_name = response_sub['pubsubChannelName']

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
                        if status == 'error':
                            error = message['error']
                        elif status == 'finished':
                            result = self.download_task_result(task_name=task_name, task_job_id=task_job_id)
                        status = message['status']
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
        
        if task_type == 'calculation':
            task_job_id = _sha1_of_string(_json_stringify_deterministic({
                'taskName': task_name,
                'taskInput': task_input
            }))
        else:
            task_job_id = _sha1_of_string(_random_string(100))
        payload = {
            'type': 'publishToPubsubChannel',
            'channelName': 'requestTasks',
            'message': {
                'type': 'requestTask',
                'taskType': task_type,
                'taskName': task_name,
                'taskInput': task_input,
                'taskJobId': task_job_id
            }
        }
        if self._project_id is not None:
            payload['projectId'] = self._project_id
        _kacherycloud_request(payload)
        
        announced_started = False
        try:
            while True:
                listener.wait(0.1)
                if status == 'finished':
                    return result
                elif status == 'error':
                    raise Exception(error)
                elif status == 'started':
                    if not announced_started:
                        print('Task started')
                        announced_started = True
        finally:
            listener.stop()

    def listen_for_task_requests(self, callback: TaskRequestCallback):
        def subscribe_to_request_tasks_channel():
            payload = {
                'type': 'subscribeToPubsubChannel',
                'channelName': 'requestTasks'
            }
            if self._project_id is not None:
                payload['projectId'] = self._project_id
            return _kacherycloud_request(payload)
        def renew_access_token():
            r = subscribe_to_request_tasks_channel()
            return r['token']
        def handle_message(*, channel: str, message: dict):
            if message['type'] == 'requestTask':
                task_type = message['taskType']
                task_name = message['taskName']
                task_input = message['taskInput']
                task_job_id = message['taskJobId']
                if task_type == 'calculation':
                    check_task_job_id = _sha1_of_string(_json_stringify_deterministic({
                        'taskName': task_name,
                        'taskInput': task_input
                    }))
                    if check_task_job_id != task_job_id:
                        raise Exception('Mismatch between task job ID and computed task job ID')
                callback(task_type=task_type, task_name=task_name, task_input=task_input, task_job_id=task_job_id)
                
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

def _random_string(num_chars: int) -> str:
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(num_chars))