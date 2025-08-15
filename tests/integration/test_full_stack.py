
import pytest
import subprocess
import time
import os
import sys
import asyncio
import json
import threading
from client.client import MCPClient

MCP_CONFIG_PATH = "tests/integration/mcp.json"

# --- Subscription Event Flow Integration Tests ---

@pytest.mark.asyncio
async def test_subscription_event_flow(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    # Monkeypatch call_subscription to yield demo events
    def test_call_subscription(self, topic, payload=None):
        import time
        if topic == 'demo_subscription':
            for i in range(3):
                event = {
                    "event": f"demo_event_{i}",
                    "data": payload or {},
                    "timestamp": time.time(),
                }
                time.sleep(0.1)
                yield event
        else:
            time.sleep(0.5)
            return
    import types
    client.call_subscription = types.MethodType(test_call_subscription, client)
    handle = client.subscriptions.subscribe('demo_subscription')
    received = []
    try:
        for _ in range(3):
            msg = handle.get(timeout=2)
            received.append(msg)
        for i, msg in enumerate(received):
            assert msg['event'] == f'demo_event_{i}'
            assert 'timestamp' in msg
    finally:
        handle.stop()

@pytest.mark.asyncio
async def test_subscription_unsubscribe(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    # Monkeypatch call_subscription to yield demo events
    def test_call_subscription(self, topic, payload=None):
        import time
        if topic == 'demo_subscription':
            for i in range(3):
                event = {
                    "event": f"demo_event_{i}",
                    "data": payload or {},
                    "timestamp": time.time(),
                }
                time.sleep(0.1)
                yield event
        else:
            time.sleep(0.5)
            return
    import types
    client.call_subscription = types.MethodType(test_call_subscription, client)
    handle = client.subscriptions.subscribe('demo_subscription')
    msg = handle.get(timeout=2)
    # Simulate unsubscribe (stop the thread)
    handle.stop()
    # After unsubscribe, no more events should be received (queue should block and timeout)
    with pytest.raises(Exception):
        handle.get(timeout=1)

@pytest.mark.asyncio
async def test_subscription_invalid_topic(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    # Monkeypatch call_subscription to yield no events for invalid topic
    def test_call_subscription(self, topic, payload=None):
        import time
        if topic == 'demo_subscription':
            for i in range(3):
                event = {
                    "event": f"demo_event_{i}",
                    "data": payload or {},
                    "timestamp": time.time(),
                }
                time.sleep(0.1)
                yield event
        else:
            time.sleep(0.5)
            return
    import types
    client.call_subscription = types.MethodType(test_call_subscription, client)
    handle = client.subscriptions.subscribe('not_a_real_topic')
    with pytest.raises(Exception):
        handle.get(timeout=1)
    handle.stop()

@pytest.fixture(scope="module")
def mcp_server():
    env = os.environ.copy()
    venv_site = '/Users/joshuawink/Documents/github/fastmcp-templates/.venv/lib/python3.13/site-packages'
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    env['PYTHONPATH'] = f"{venv_site}:{project_root}"
    env['PATH'] = f"/Users/joshuawink/Documents/github/fastmcp-templates/.venv/bin:" + env.get('PATH', '')
    proc = subprocess.Popen([
        sys.executable, "server/server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=project_root, env=env)
    time.sleep(2)
    yield proc
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()

@pytest.mark.asyncio
async def test_resource_fetch(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    async with client._client:
        resources = await client.discovery.list_resources()
        assert isinstance(resources, list)
        # Extract string URI if resource is an object
        uris = [r.uri if hasattr(r, 'uri') else r for r in resources]
        if uris:
            data = await client.resources.get(uris[0])
            assert data is not None

@pytest.mark.asyncio
async def test_prompt_render(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    async with client._client:
        prompts = await client.discovery.list_prompts()
        assert isinstance(prompts, list)
        # Extract string name if prompt is an object
        names = [p.name if hasattr(p, 'name') else p for p in prompts]
        if names:
            # Use only supported arguments for the demo prompt
            result = await client.prompts.render(names[0], name="IntegrationTest")
            assert result is not None


@pytest.mark.asyncio
async def test_subscription_handler(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    async with client._client:
        result = await client._client.call_tool('list_demo_capabilities')
        # Parse JSON string from TextContent
        caps = json.loads(result.content[0].text)
        assert 'subscriptions' in caps
        assert 'demo_subscription' in caps['subscriptions']


@pytest.mark.asyncio
async def test_error_handling(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    async with client._client:
        with pytest.raises(Exception):
            await client.tools.raise_error()

@pytest.mark.asyncio
async def test_schema_discovery(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    async with client._client:
        resources = await client.discovery.list_resources()
        uris = [r.uri if hasattr(r, 'uri') else r for r in resources]
        schema_uris = [u for u in uris if isinstance(u, str) and u.startswith("schema://")] 
        if schema_uris:
            schema = await client.resources.get(schema_uris[0])
            assert isinstance(schema, dict)
            assert "type" in schema


@pytest.mark.asyncio
async def test_auth_provider(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    async with client._client:
        result = await client._client.call_tool('list_demo_capabilities')
        caps = json.loads(result.content[0].text)
        assert 'auth' in caps
        assert 'demo_auth' in caps['auth']


@pytest.mark.asyncio
async def test_capabilities_listing(mcp_server):
    client = MCPClient(MCP_CONFIG_PATH)
    async with client._client:
        result = await client._client.call_tool('list_demo_capabilities')
        caps = json.loads(result.content[0].text)
        assert 'tools' in caps
        assert 'resources' in caps
        assert 'prompts' in caps
        assert 'subscriptions' in caps
        assert 'auth' in caps
