import pytest
from server.app.prompts import register_prompts
from tests.helpers import DummyServer

def test_hello_prompt():
    server = DummyServer()
    register_prompts(server)
    assert "hello_prompt" in server._prompts
    result = server._prompts["hello_prompt"]("Test")
    assert result == "Prompt says: Hello, Test!"
