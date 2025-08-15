import pytest
from server.app.discovery import register_discovery
from tests.helpers import DummyServer

def test_list_demo_capabilities():
    server = DummyServer()
    # Pre-register demo items so the discovery tool can find them
    server._tools["hello_tool"] = lambda: None
    server._resources["resource://hello_resource"] = lambda: None
    server._prompts["hello_prompt"] = lambda: None
    server._subscriptions["demo_subscription"] = lambda payload: None
    server._auth_providers["demo_auth"] = lambda token: None
    register_discovery(server)
    assert "list_demo_capabilities" in server._tools
    result = server._tools["list_demo_capabilities"]()
    # The result is a dict of lists, e.g. {'tools': [...], 'resources': [...], ...}
    assert "tools" in result and "hello_tool" in result["tools"]
    assert "resources" in result and "resource://hello_resource" in result["resources"]
    assert "prompts" in result and "hello_prompt" in result["prompts"]
    assert "subscriptions" in result and "demo_subscription" in result["subscriptions"]
    assert "auth" in result and "demo_auth" in result["auth"]
