import pytest
import threading
import queue
from client.app.subscribe import SubscriptionClient, SubscriptionHandle

class DummyWrapper:
    def __init__(self):
        self.events = [
            {"event": "test_event_1", "data": {}, "timestamp": 1},
            {"event": "test_event_2", "data": {}, "timestamp": 2},
        ]
    def subscribe(self, topic, payload=None):
        for event in self.events:
            yield event

def test_subscribe_returns_handle_and_receives_events():
    wrapper = DummyWrapper()
    client = type('Dummy', (), {"_client": wrapper})()
    sub = SubscriptionClient(client)
    received = []
    handle = sub.subscribe('any_topic', callback=received.append)
    # Wait for events to be processed
    for _ in range(2):
        msg = handle.get(timeout=1)
        assert msg["event"].startswith("test_event_")
    handle.stop()
    assert len(received) == 2

def test_subscribe_handle_stop():
    wrapper = DummyWrapper()
    client = type('Dummy', (), {"_client": wrapper})()
    sub = SubscriptionClient(client)
    handle = sub.subscribe('any_topic')
    handle.stop()
    assert not handle._thread.is_alive()
