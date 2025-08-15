import pytest
from client.app.llm_router import LLMRouter

class DummyTools:
    def call(self, name, **kwargs):
        return f"tool:{name}:{kwargs}"

class DummyPrompts:
    def render(self, name, **kwargs):
        return f"prompt:{name}:{kwargs}"

class DummyResources:
    def get(self, name):
        return f"resource:{name}"

class DummyDiscovery:
    def list_tools(self):
        return ["foo", "bar"]
    def list_prompts(self):
        return ["baz", "qux"]
    def list_resources(self):
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

def test_route_tool(router):
    msg = {"tool": "foo", "args": {"x": 1}}
    assert router.route(msg) == "tool:foo:{'x': 1}"

def test_route_prompt(router):
    msg = {"prompt": "baz", "args": {"y": 2}}
    assert router.route(msg) == "prompt:baz:{'y': 2}"

def test_route_resource(router):
    msg = {"resource": "file"}
    assert router.route(msg) == "resource:file"

def test_route_unknown(router):
    with pytest.raises(ValueError):
        router.route({"unknown": "foo"})

def test_route_batch_sequential(router):
    msgs = [
        {"tool": "foo", "args": {"a": 1}},
        {"prompt": "baz", "args": {"b": 2}},
        {"resource": "file"},
    ]
    results = router.route_batch(msgs)
    assert results == [
        "tool:foo:{'a': 1}",
        "prompt:baz:{'b': 2}",
        "resource:file",
    ]

def test_route_batch_parallel(router):
    msgs = [
        {"tool": "foo", "args": {"a": 1}},
        {"prompt": "baz", "args": {"b": 2}},
        {"resource": "file"},
    ]
    results = router.route_batch(msgs, parallel=True)
    # Order may not be preserved in parallel, so sort for comparison
    assert sorted(results) == sorted([
        "tool:foo:{'a': 1}",
        "prompt:baz:{'b': 2}",
        "resource:file",
    ])

def test_get_llm_capabilities(router):
    caps = router.get_llm_capabilities()
    assert "foo" in caps and "baz" in caps and "file" in caps

def test_route_json_string_tool(router):
    msg = '{"tool": "foo", "args": {"z": 3}}'
    assert router.route(msg) == "tool:foo:{'z': 3}"

def test_route_json_string_resource(router):
    msg = '{"resource": "file"}'
    assert router.route(msg) == "resource:file"

def test_route_json_string_invalid(router):
    msg = '{"unknown": "foo"}'
    with pytest.raises(ValueError):
        router.route(msg)
