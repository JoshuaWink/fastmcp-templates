
import pytest
from tests.utilities.llm_test_utils import llm_call, LLM_MODEL

@pytest.mark.integration
def test_llm_tool_call():
    messages = [
        {"role": "system", "content": "You are an agent. When you need to call a tool, respond ONLY in JSON using: {\"tool\": \"TOOL_NAME\", \"args\": { ... }}."},
        {"role": "user", "content": "Call the foo tool with x=1."}
    ]
    result = llm_call(messages)
    assert '"tool": "foo"' in result or (isinstance(result, dict) and result["tool"] == "foo")
    assert '"x": 1' in result or (isinstance(result, dict) and result["args"]["x"] == 1)

@pytest.mark.integration
def test_llm_prompt_call():
    messages = [
        {"role": "system", "content": "You are an agent. When you need to call a prompt, respond ONLY in JSON using: {\"prompt\": \"PROMPT_NAME\", \"args\": { ... }}."},
        {"role": "user", "content": "Call the baz prompt with y=2."}
    ]
    result = llm_call(messages)
    assert '"prompt": "baz"' in result or (isinstance(result, dict) and result["prompt"] == "baz")
    assert '"y": 2' in result or (isinstance(result, dict) and result["args"]["y"] == 2)
