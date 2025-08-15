import pytest
from server.app.tools import register_tools

class DummyServer:
    def __init__(self):
        self._tools = {}
    def tool(self, name, description):
        def decorator(fn):
            self._tools[name] = fn
            return fn
        return decorator

def test_hello_tool():
    server = DummyServer()
    register_tools(server)
    assert "hello_tool" in server._tools
    result = server._tools["hello_tool"]("Test")
    assert result == "Hello, Test!"
