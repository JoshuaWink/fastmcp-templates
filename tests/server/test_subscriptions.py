import pytest
from server.app.subscriptions import register_subscriptions, current_utc_timestamp
from tests.helpers import DummyServer

def test_demo_subscription_handler():
    import asyncio
    server = DummyServer()
    register_subscriptions(server)
    assert "demo_subscription" in server._subscriptions
    payload = {"foo": "bar"}
    async def get_first_event():
        agen = server._subscriptions["demo_subscription"](payload)
        async for event in agen:
            return event
    result = asyncio.run(get_first_event())
    assert result["event"].startswith("demo_event")
    assert result["data"] == payload
    assert isinstance(result["timestamp"], float)
    # Timestamp should be close to now
    assert abs(result["timestamp"] - current_utc_timestamp()) < 2
