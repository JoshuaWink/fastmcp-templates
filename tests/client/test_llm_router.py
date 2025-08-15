import pytest
from client.app.llm_router import LLMRouter

class DummyTools:
    async def call(self, name, **kwargs):
        return f"tool:{name}:{kwargs}"

class DummyPrompts:
    async def render(self, name, **kwargs):
        return f"prompt:{name}:{kwargs}"

class DummyResources:
    async def get(self, name):
        return f"resource:{name}"

class DummyDiscovery:
    async def list_tools(self):
        return ["foo", "bar"]
    async def list_prompts(self):
        return ["baz", "qux"]
    async def list_resources(self):
        return ["file", "db"]

class DummyClient:
    def __init__(self):
        self.tools = DummyTools()
        self.prompts = DummyPrompts()
        self.resources = DummyResources()
        self.discovery = DummyDiscovery()

@pytest.fixture
def router():
    return LLMRouter(DummyClient())

import pytest

@pytest.mark.asyncio
async def test_route_tool(router):
    msg = {"tool": "foo", "args": {"x": 1}}
    assert await router.route(msg) == "tool:foo:{'x': 1}"

@pytest.mark.asyncio
async def test_route_prompt(router):
    msg = {"prompt": "baz", "args": {"y": 2}}
    assert await router.route(msg) == "prompt:baz:{'y': 2}"

@pytest.mark.asyncio
async def test_route_resource(router):
    msg = {"resource": "file"}
    assert await router.route(msg) == "resource:file"

@pytest.mark.asyncio
async def test_route_unknown(router):
    with pytest.raises(ValueError):
        await router.route({"unknown": "foo"})

@pytest.mark.asyncio
async def test_route_batch_sequential(router):
    msgs = [
        {"tool": "foo", "args": {"a": 1}},
        {"prompt": "baz", "args": {"b": 2}},
        {"resource": "file"},
    ]
    results = await router.route_batch(msgs)
    assert results == [
        "tool:foo:{'a': 1}",
        "prompt:baz:{'b': 2}",
        "resource:file",
    ]

@pytest.mark.asyncio
async def test_route_batch_parallel(router):
    msgs = [
        {"tool": "foo", "args": {"a": 1}},
        {"prompt": "baz", "args": {"b": 2}},
        {"resource": "file"},
    ]
    results = await router.route_batch(msgs, parallel=True)
    # Order may not be preserved in parallel, so sort for comparison
    assert sorted(results) == sorted([
        "tool:foo:{'a': 1}",
        "prompt:baz:{'b': 2}",
        "resource:file",
    ])

@pytest.mark.asyncio
async def test_get_llm_capabilities(router):
    caps = await router.get_llm_capabilities()
    # The result is a JSON string, so parse it
    import json
    caps_dict = json.loads(caps)
    assert "foo" in caps_dict["tools"] and "baz" in caps_dict["prompts"] and "file" in caps_dict["resources"]

@pytest.mark.asyncio
async def test_route_json_string_tool(router):
    msg = '{"tool": "foo", "args": {"z": 3}}'
    assert await router.route(msg) == "tool:foo:{'z': 3}"

@pytest.mark.asyncio
async def test_route_json_string_resource(router):
    msg = '{"resource": "file"}'
    assert await router.route(msg) == "resource:file"

@pytest.mark.asyncio
async def test_route_json_string_invalid(router):
    msg = '{"unknown": "foo"}'
    with pytest.raises(ValueError):
        await router.route(msg)
