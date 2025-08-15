import pytest
from server.app.resources import register_resources

class DummyServer:
    def __init__(self):
        self._resources = {}
    def resource(self, uri, name, description):
        def decorator(fn):
            self._resources[uri] = fn
            return fn
        return decorator

def test_hello_resource():
    server = DummyServer()
    register_resources(server)
    assert "resource://hello_resource" in server._resources
    result = server._resources["resource://hello_resource"]()
    assert result == "Hello from the resource!"
