import time
from typing import List, Union

from kachery_cloud.TaskBackend.PubsubListener import PubsubListener
from kachery_cloud.load_file import _random_string
from .._kacherycloud_request import _kacherycloud_request
from ..get_client_id import get_client_id
from .._client_keys import _deterministic_json_dumps


class Feed:
    def __init__(self, *, feed_id: str, project_id: str) -> None:
        self._feed_id = feed_id
        self._project_id = project_id
        self._current_message_number = 0
        self._pubsub_listener: Union[PubsubListener, None] = None
        self._project_id = project_id
        self._messages_appended_callbacks = {}
    def append_message(self, message: dict):
        self.append_messages([message])
    def append_messages(self, messages: List[dict]):
        payload = {
            'type': 'appendFeedMessages',
            'feedId': self._feed_id,
            'messagesJson': [_deterministic_json_dumps(x) for x in messages]
        }
        resp = _kacherycloud_request(payload)
    @property
    def uri(self):
        return f'kachery-feed://{self._feed_id}'
    @property
    def feed_id(self):
        return self._feed_id
    @property
    def current_message_number(self):
        return self._current_message_number
    def set_position(self, position: int):
        self._current_message_number = position
    def get_next_messages(self, *, timeout_sec: float=0) -> List[dict]:
        payload = {
            'type': 'getFeedMessages',
            'feedId': self._feed_id,
            'startMessageNumber': self._current_message_number
        }
        resp = _kacherycloud_request(payload)
        messages = resp['messages']
        if len(messages) == 0 and timeout_sec > 0:
            return self._wait_for_next_messages(timeout_sec=timeout_sec)
        start_message_number = resp['startMessageNumber']
        self._current_message_number = start_message_number + len(messages)
        return messages
    @staticmethod
    def create(*, project_id: Union[str, None]=None):
        payload = {
            'type': 'createFeed'
        }
        if project_id is not None:
            payload['projectId'] = project_id
        response = _kacherycloud_request(payload)
        feed_id = response['feedId']
        project_id = response['projectId']
        return Feed(feed_id=feed_id, project_id=project_id)
    @staticmethod
    def load(feed_id_or_uri: str):
        if feed_id_or_uri.startswith('kachery-feed://'):
            feed_id = feed_id_or_uri.split('/')[2]
        else:
            feed_id = feed_id_or_uri
        payload = {
            'type': 'getFeedInfo',
            'feedId': feed_id
        }
        response = _kacherycloud_request(payload)
        project_id = response['projectId']
        return Feed(feed_id=feed_id, project_id=project_id)
    def _wait_for_next_messages(self, *, timeout_sec: float):
        timer = time.time()
        if self._pubsub_listener is None:
            self._initialize_pubsub_listener()
        callback_id = _random_string(10)
        got_new_messages = False
        def on_new_messages():
            nonlocal got_new_messages
            got_new_messages = True
        self._messages_appended_callbacks[callback_id] = on_new_messages
        try:
            messages0 = self.get_next_messages()
            if len(messages0) > 0:
                return messages0
            while True:
                if got_new_messages:
                    messages1 = self.get_next_messages()
                    if len(messages1) > 0:
                        return messages1
                elapsed = time.time() - timer
                if elapsed > timeout_sec:
                    return []
                self._pubsub_listener.wait(0.05)
        finally:
            del self._messages_appended_callbacks[callback_id]
        
    def _initialize_pubsub_listener(self):
        client_id = get_client_id()

        def subscribe_to_channel():
            payload_sub = {
                'type': 'subscribeToPubsubChannel',
                'channelName': 'feedUpdates',
                'projectId': self._project_id
            }
            response_sub = _kacherycloud_request(payload_sub)
            return response_sub
        
        response_sub = subscribe_to_channel()
        subscribe_key = response_sub['subscribeKey']
        subscribe_token = response_sub['token']
        pubsub_channel_name = response_sub['pubsubChannelName']

        def handle_message(*, channel: str, message: dict):
            if message['type'] == 'feedMessagesAppended':
                if message['feedId'] == self._feed_id:
                    callbacks = self._messages_appended_callbacks.values()
                    for cb in callbacks:
                        cb()
        def renew_access_token():
            r = subscribe_to_channel()
            return r['token']
        listener = PubsubListener(
            channels=[pubsub_channel_name],
            uuid=client_id,
            subscribe_key=subscribe_key,
            access_token=subscribe_token,
            renew_access_token_callback=renew_access_token
        )
        listener.on_message(handle_message)
        listener.start()
        self._pubsub_listener = listener