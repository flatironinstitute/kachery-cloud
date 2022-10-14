import time
from typing import List, Union

from ..TaskBackend.PubsubListener import PubsubListener
from ..get_project_id import get_project_id
from ..load_file import _random_string
from .._kacherycloud_request import _kacherycloud_request
from ..get_client_id import get_client_id
from .._client_keys import _deterministic_json_dumps


class Feed:
    def __init__(self, *, feed_id: str, project_id: str) -> None:
        self._feed_id = feed_id
        self._project_id = project_id
        self._current_message_number = 0
        self._messages = []
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
        if self._current_message_number < len(self._messages):
            ret = self._messages[self._current_message_number:]
            self._current_message_number = len(self._messages)
            return ret
        num = len(self._messages)
        payload = {
            'type': 'getFeedMessages',
            'feedId': self._feed_id,
            'startMessageNumber': num
        }
        resp = _kacherycloud_request(payload)
        messages = resp['messages']
        if len(messages) > 0:
            for ii in range(len(messages)):
                if num + ii == len(self._messages):
                    self._messages.append(messages[ii])
            return self.get_next_messages(timeout_sec=0)
        elif timeout_sec > 0:
            got_new = self._wait_for_next_messages(timeout_sec=timeout_sec)
            if got_new:
                return self.get_next_messages(timeout_sec=0)
            else:
                return []
        else:
            return []
    @staticmethod
    def create(*, project_id: Union[str, None]=None):
        payload = {
            'type': 'createFeed'
        }
        if project_id is not None:
            payload['projectId'] = project_id
        else:
            payload['projectId'] = get_project_id()
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
            while True:
                if got_new_messages:
                    return True
                elapsed = time.time() - timer
                if elapsed > timeout_sec:
                    return False
                time.sleep(0.05)
                # self._pubsub_listener.wait(0.05)
        finally:
            del self._messages_appended_callbacks[callback_id]
        
    def _initialize_pubsub_listener(self):
        pass
        # client_id = get_client_id()

        # def subscribe_to_channel():s
        #     payload_sub = {
        #         'type': 'subscribeToPubsubChannel',
        #         'channelName': 'feedUpdates',
        #         'projectId': self._project_id
        #     }
        #     response_sub = _kacherycloud_request(payload_sub)
        #     return response_sub
        
        # response_sub = subscribe_to_channel()
        # subscribe_key = response_sub['subscribeKey']
        # subscribe_token = response_sub['token']
        # pubsub_channel_name = response_sub['pubsubChannelName']

        # def handle_message(*, channel: str, message: dict):
        #     if message['type'] == 'feedMessagesAppended':
        #         if message['feedId'] == self._feed_id:
        #             callbacks = self._messages_appended_callbacks.values()
        #             for cb in callbacks:
        #                 cb()
        # def renew_access_token():
        #     r = subscribe_to_channel()
        #     return r['token']
        # listener = PubsubListener(
        #     channels=[pubsub_channel_name],
        #     uuid=client_id,
        #     subscribe_key=subscribe_key,
        #     access_token=subscribe_token,
        #     renew_access_token_callback=renew_access_token
        # )
        # listener.on_message(handle_message)
        # listener.start()
        # self._pubsub_listener = listener