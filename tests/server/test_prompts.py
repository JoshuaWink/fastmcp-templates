import pytest
from server.app.prompts import register_prompts

class DummyServer:
    def __init__(self):
        self._prompts = {}
    def prompt(self, name, description):
        def decorator(fn):
            self._prompts[name] = fn
            return fn
        return decorator

def test_hello_prompt():
    server = DummyServer()
    register_prompts(server)
    assert "hello_prompt" in server._prompts
    result = server._prompts["hello_prompt"]("Test")
    assert result == "Prompt says: Hello, Test!"
