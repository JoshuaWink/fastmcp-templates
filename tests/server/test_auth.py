import pytest
from server.app.auth import register_auth

class DummyServer:
    def __init__(self):
        self._auths = {}
    def auth(self, name, description):
        def decorator(fn):
            self._auths[name] = fn
            return fn
        return decorator

def test_demo_auth_provider():
    server = DummyServer()
    register_auth(server)
    assert "demo_auth_provider" in server._auths
    fn = server._auths["demo_auth_provider"]
    assert fn("demo_user", "password123") is True
    assert fn("wrong", "password123") is False
    assert fn("demo_user", "wrong") is False
