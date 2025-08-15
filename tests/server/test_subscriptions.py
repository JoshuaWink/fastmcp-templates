import pytest
from server.app.subscriptions import register_subscriptions, current_utc_timestamp

class DummyServer:
    def __init__(self):
        self._subscriptions = {}
    def subscription(self, name, description):
        def decorator(fn):
            self._subscriptions[name] = fn
            return fn
        return decorator

def test_demo_subscription_handler():
    server = DummyServer()
    register_subscriptions(server)
    assert "demo_subscription" in server._subscriptions
    payload = {"foo": "bar"}
    result = server._subscriptions["demo_subscription"](payload)
    assert result["event"] == "demo_event"
    assert result["data"] == payload
    assert isinstance(result["timestamp"], float)
    # Timestamp should be close to now
    assert abs(result["timestamp"] - current_utc_timestamp()) < 2
