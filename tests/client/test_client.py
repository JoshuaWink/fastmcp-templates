import pytest
from client.client import MCPClient

class DummyFastMCP:
    async def call_tool(self, tool_name, kwargs):
        if tool_name == 'echo':
            return kwargs
        if tool_name == 'greet':
            user = kwargs.get('user', 'World')
            return f"Hello, {user}!"
        return None

    async def read_resource(self, resource_name):
        if resource_name == 'file':
            return 'data'
        return None

    async def render_prompt(self, prompt_name, kwargs):
        if prompt_name == 'greet':
            return f"Hello, {kwargs.get('user', 'World')}!"
        return None

    async def list_tools(self):
        return ['tool1', 'tool2']

    async def list_resources(self):
        return ['res1', 'file']

    async def list_prompts(self):
        return ['prompt1', 'greet']

    def log(self, message, level='info'):
        return f'LOG:{level}:{message}'

    def progress(self, progress, detail=None):
        return f'PROGRESS:{progress}:{detail}'

    def elicit(self, schema, prompt=None):
        return {'input': 'test'}

@pytest.fixture
def dummy_client(monkeypatch):
    # Patch MCPClient to use DummyFastMCP
    monkeypatch.setattr('client.client.FastMCPClient', lambda *args, **kwargs: DummyFastMCP())
    dummy_config = {"mcpServers": {"dummy": {"type": "dummy"}}}
    return MCPClient(dummy_config)

import pytest

@pytest.mark.asyncio
async def test_tools_call(dummy_client):
    result = await dummy_client.tools.call('echo', foo='bar')
    assert result == {'foo': 'bar'}

@pytest.mark.asyncio
async def test_resources_get(dummy_client):
    result = await dummy_client.resources.get('file')
    assert result == 'data'

@pytest.mark.asyncio
async def test_prompts_render(dummy_client):
    result = await dummy_client.prompts.render('greet', user='Alice')
    assert result == 'Hello, Alice!'

@pytest.mark.asyncio
async def test_discovery_lists(dummy_client):
    assert await dummy_client.discovery.list_tools() == ['tool1', 'tool2']
    assert await dummy_client.discovery.list_resources() == ['res1', 'file']
    assert await dummy_client.discovery.list_prompts() == ['prompt1', 'greet']

def test_logging(dummy_client):
    assert dummy_client.logging.log('msg', level='warn') == 'LOG:warn:msg'


def test_elicitation(dummy_client):
    assert dummy_client.elicitation.request({'type': 'string'}) == {'input': 'test'}

def test_notifications(dummy_client):
    dummy_client.notifications.add_notification('low', priority='low')
    dummy_client.notifications.add_notification('critical', priority='critical')
    notes = dummy_client.notifications.get_notifications()
    assert any('critical' in n for n in notes)
    dummy_client.notifications.clear_notifications('low')
    notes = dummy_client.notifications.get_notifications()
    assert all('low' not in n for n in notes)

@pytest.mark.asyncio
async def test_llm_simulated_tool_call(dummy_client):
    """
    Simulate an LLM calling the 'greet' tool and check the output matches what an LLM would expect.
    """
    result = await dummy_client.prompts.render('greet', user='Ford')
    assert result == 'Hello, Ford!'


import pytest

@pytest.mark.asyncio
async def test_llm_json_tool_call(dummy_client):
    from client.app.llm_router import LLMRouter
    router = LLMRouter(dummy_client)
    llm_json = '{"tool": "greet", "args": {"user": "Ford"}}'
    result = await router.route(llm_json)
    assert result == 'Hello, Ford!'


@pytest.mark.asyncio
async def test_llm_json_resource_call(dummy_client):
    from client.app.llm_router import LLMRouter
    router = LLMRouter(dummy_client)
    llm_json = '{"resource": "file"}'
    result = await router.route(llm_json)
    assert result == 'data'


@pytest.mark.asyncio
async def test_llm_capabilities_exposed(dummy_client):
    from client.app.llm_router import LLMRouter
    import json
    router = LLMRouter(dummy_client)
    caps = json.loads(await router.get_llm_capabilities())
    assert 'greet' in caps['prompts']
    assert 'echo' in caps['tools'] or 'tool1' in caps['tools']
    assert 'file' in caps['resources']
