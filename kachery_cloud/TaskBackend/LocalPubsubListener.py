import time
from typing import List
import simplejson
from .PubsubListener import MessageCallback
import requests


class LocalPubsubListener:
    def __init__(self, *, channel: str, port: int) -> None:
        self._channel = channel
        self._port = port
        self._message_callbacks: List[MessageCallback] = []
        self._stopped = False
        self._last_message_id = ''
    def on_message(self, callback: MessageCallback):
        self._message_callbacks.append(callback)
    def start(self):
        pass
    def wait(self, timeout_sec: float):
        req = {'type': 'subscribe', 'channel': self._channel, 'timeoutMsec': timeout_sec * 1000, 'lastMessageId': self._last_message_id}
        failed_at_least_once = False
        while True:
            try:
                resp = requests.post(f'http://localhost:{self._port}', json=req)
                if resp.status_code != 200:
                    raise Exception(f'Error in pubsub request')
                if failed_at_least_once:
                    print('Connected to local pubsub server')
                break
            except Exception as err:
                print('Error connecting to local pubsub server. Trying again in 5 seconds.', str(err))
                failed_at_least_once = True
                time.sleep(5)
        response = resp.json()
        messages = response['messages']
        for m in messages:
            message_body = m['messageBody']
            message_id = m['messageId']
            message_json = simplejson.loads(message_body)
            self._last_message_id = message_id
            for cb in self._message_callbacks:
                cb(channel=self._channel, message=message_json)
        if len(messages) == 0:
            time.sleep(timeout_sec)
    def stop(self):
        self._stopped = True
        time.sleep(1)