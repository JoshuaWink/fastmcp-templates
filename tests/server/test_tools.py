import pytest
from server.app.tools import register_tools
from tests.helpers import DummyServer

def test_hello_tool():
    server = DummyServer()
    register_tools(server)
    assert "hello_tool" in server._tools
    result = server._tools["hello_tool"]("Test")
    assert result == "Hello, Test!"
