import pytest
from server.app.discovery import register_discovery

class DummyServer:
    def __init__(self):
        self._tools = {}
    def tool(self, name, description):
        def decorator(fn):
            self._tools[name] = fn
            return fn
        return decorator

def test_list_demo_capabilities():
    server = DummyServer()
    register_discovery(server)
    assert "list_demo_capabilities" in server._tools
    result = server._tools["list_demo_capabilities"]()
    assert "tools" in result and "hello_tool" in result["tools"]
    assert "resources" in result and "hello_resource" in result["resources"]
    assert "prompts" in result and "hello_prompt" in result["prompts"]
    assert "subscriptions" in result and "demo_subscription" in result["subscriptions"]
    assert "auth" in result and "demo_auth_provider" in result["auth"]
