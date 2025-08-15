import pytest
from server.app.error_handling import register_error_handlers

class DummyServer:
    def __init__(self):
        self._error_handlers = {}
    def error_handler(self, name, description):
        def decorator(fn):
            self._error_handlers[name] = fn
            return fn
        return decorator

def test_demo_error_handler():
    server = DummyServer()
    register_error_handlers(server)
    assert "demo_error_handler" in server._error_handlers
    # Simulate an error
    error = Exception("Test error")
    result = server._error_handlers["demo_error_handler"](error)
    assert result == {"error": "Test error"}
