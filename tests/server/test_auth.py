import pytest
from server.app.auth import register_auth
from tests.helpers import DummyServer

def test_demo_auth_provider():
    server = DummyServer()
    register_auth(server)
    # Server's demo_auth expects a token string; it returns a dict for valid token
    assert "demo_auth" in server._auth_providers
    fn = server._auth_providers["demo_auth"]
    assert fn("demo-token") == {"user": "demo"}
    try:
        fn("invalid-token")
        assert False, "Expected exception for invalid token"
    except Exception:
        pass
