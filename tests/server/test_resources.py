import pytest
from server.app.resources import register_resources
from tests.helpers import DummyServer

def test_hello_resource():
    server = DummyServer()
    register_resources(server)
    assert "resource://hello_resource" in server._resources
    result = server._resources["resource://hello_resource"]()
    assert result == "Hello from the resource!"
