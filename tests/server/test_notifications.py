import pytest
from server.app.notifications import register_notifications
from tests.helpers import DummyServer

def test_demo_notification_handler():
    server = DummyServer()
    register_notifications(server)
    assert "demo_notification" in server._subscriptions
    result = server._subscriptions["demo_notification"]("Test message", "high")
    assert result["type"] == "notification"
    assert result["message"] == "Test message"
    assert result["priority"] == "high"
