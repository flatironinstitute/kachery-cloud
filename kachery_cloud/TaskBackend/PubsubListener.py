from typing import Any, List, Protocol
import time

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory

from pubnub.models.consumer.pubsub import PNMessageResult


class MessageCallback(Protocol):
    def __call__(self, *, channel: str, message: Any): ...

class RenewAccessTokenCallback(Protocol):
    def __call__(self) -> str: ...

class PubsubListener:
    def __init__(self,
        *,
        channels: List[str],
        uuid: str,
        access_token: str,
        renew_access_token_callback: RenewAccessTokenCallback,
        subscribe_key: str
    ) -> None:
        self._channels = channels
        self._uuid = uuid
        self._access_token = access_token
        self._renew_access_token_callback = renew_access_token_callback
        self._subscribe_key = subscribe_key
        self._message_callbacks: List[MessageCallback] = []
        self._ttl = None
        self._ttl_timestamp = None
    def on_message(self, callback: MessageCallback):
        self._message_callbacks.append(callback)
    def start(self):
        # token = self._get_access_token_callback(uuid=self._uuid, channel_names=self._channels)
        token = self._access_token

        pnconfig = PNConfiguration()

        pnconfig.subscribe_key = self._subscribe_key
        pnconfig.uuid = self._uuid
        self._pubnub = PubNub(pnconfig)
        self._pubnub.set_token(token)

        self._ttl = self._pubnub.parse_token(token)['ttl']
        self._ttl_timestamp = time.time()

        self._pubnub.add_listener(MySubscribeCallback(listener=self))

        self._pubnub.subscribe().channels(self._channels).execute()
    def wait(self, timeout_sec: float):
        self._check_token()
        time.sleep(timeout_sec)
    def stop(self):
        self._pubnub.unsubscribe_all()
        time.sleep(1)
    def _check_token(self):
        if self._ttl is None:
            return
        elapsed_min = (time.time() - self._ttl_timestamp) / 60
        if elapsed_min + 1 > self._ttl:
            new_token = self._renew_access_token_callback()
            self._ttl = self._pubnub.parse_token(new_token)['ttl']
            self._ttl_timestamp = time.time()
            self._pubnub.set_token(new_token)

class MySubscribeCallback(SubscribeCallback):
    def __init__(self, listener: PubsubListener) -> None:
        self._listener = listener
        super().__init__()
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message: PNMessageResult):
        # Handle new message stored in message.message
        for cb in self._listener._message_callbacks:
            cb(channel=message.channel, message=message.message)