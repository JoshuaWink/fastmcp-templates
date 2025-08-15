import pytest
from client.client import MCPClient

class DummyFastMCP:
    def __init__(self):
        self.tools = type('T', (), {
            'list': lambda self: ['tool1', 'tool2'],
            'echo': lambda self, **kwargs: kwargs
        })()
        self.resources = type('R', (), {
            'list': lambda self: ['res1', 'file'],
            'file': lambda self: 'data'
        })()
        self.prompts = type('P', (), {
            'list': lambda self: ['prompt1', 'greet'],
            'greet': lambda self, user: f'Hello, {user}!'
        })()
        self.log = lambda message, level='info': f'LOG:{level}:{message}'
        self.progress = lambda progress, detail=None: f'PROGRESS:{progress}:{detail}'
        self.elicit = lambda schema, prompt=None: {'input': 'test'}

@pytest.fixture
def dummy_client(monkeypatch):
    # Patch MCPClient to use DummyFastMCP
    monkeypatch.setattr('client.client.FastMCPClient', lambda **cfg: DummyFastMCP())
    return MCPClient({})

def test_tools_call(dummy_client):
    result = dummy_client.tools.call('echo', foo='bar')
    assert result == {'foo': 'bar'}

def test_resources_get(dummy_client):
    result = dummy_client.resources.get('file')
    assert result == 'data'

def test_prompts_render(dummy_client):
    result = dummy_client.prompts.render('greet', user='Alice')
    assert result == 'Hello, Alice!'

def test_discovery_lists(dummy_client):
    assert dummy_client.discovery.list_tools() == ['tool1', 'tool2']
    assert dummy_client.discovery.list_resources() == ['res1', 'file']
    assert dummy_client.discovery.list_prompts() == ['prompt1', 'greet']

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

def test_llm_simulated_tool_call(dummy_client):
    """
    Simulate an LLM calling the 'greet' tool and check the output matches what an LLM would expect.
    """
    result = dummy_client.prompts.render('greet', user='Ford')
    assert result == 'Hello, Ford!'

def test_llm_json_tool_call(dummy_client):
    from client.llm_router import LLMRouter
    router = LLMRouter(dummy_client)
    llm_json = '{"tool": "greet", "args": {"user": "Ford"}}'
    result = router.route(llm_json)
    assert result == 'Hello, Ford!'

def test_llm_json_resource_call(dummy_client):
    from client.llm_router import LLMRouter
    router = LLMRouter(dummy_client)
    llm_json = '{"resource": "file"}'
    result = router.route(llm_json)
    assert result == 'data'

def test_llm_capabilities_exposed(dummy_client):
    from client.llm_router import LLMRouter
    import json
    router = LLMRouter(dummy_client)
    caps = json.loads(router.get_llm_capabilities())
    assert 'greet' in caps['prompts']
    assert 'echo' in caps['tools'] or 'tool1' in caps['tools']
    assert 'file' in caps['resources']
