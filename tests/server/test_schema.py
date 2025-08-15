import pytest
from server.app.schema import register_schema

class DummyServer:
    def __init__(self):
        self._schemas = {}
    def schema(self, name, description):
        def decorator(fn):
            self._schemas[name] = fn
            return fn
        return decorator

def test_demo_schema():
    server = DummyServer()
    register_schema(server)
    assert "demo_schema" in server._schemas
    result = server._schemas["demo_schema"]()
    assert isinstance(result, dict)
    assert result.get("title") == "DemoSchema"
    assert "type" in result
