import pytest
from server.app.schema import register_schema
from tests.helpers import DummyServer

def test_demo_schema():
    server = DummyServer()
    register_schema(server)
    # The resource is registered under the URI key
    assert "schema://hello_tool" in server._resources
    result = server._resources["schema://hello_tool"]()
    assert isinstance(result, dict)
    assert "type" in result
    assert "properties" in result
