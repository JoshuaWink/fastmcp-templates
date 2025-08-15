# Note: In typical LLM tool call cycles, when a tool is called, the LLM responds in JSON (as below),
# and the client/server may then send another message (with updated context or validation) after the tool call.
# This enables a multi-turn flow: user/LLM message → tool call → tool result → follow-up message.
# Our client does not yet support full context management, but this annotation clarifies the intended flow
# for future context manager integration. Attach or reference this as needed for context-aware workflows.
# Prompt template for instructing LLMs to respond in JSON format for tool/resource calls
LLM_JSON_TOOL_CALL_PROMPT = (
    "You are an agent. When you need to call a tool or resource, respond ONLY in JSON using one of these formats: "
    "For a tool or prompt: {\"tool\": \"TOOL_NAME\", \"args\": { ... }}. "
    "For a resource: {\"resource\": \"RESOURCE_NAME\"}. "
    "Do not include any extra text, explanation, or formatting. The response must be valid, compact JSON."
)


# LLM_BATCH_CHAIN_PROMPT is experimental/advanced. Enable via config: {"enable_batch_prompt": true}
LLM_BATCH_CHAIN_PROMPT = (
    "You are an agent capable of executing multiple tool, prompt, or resource calls in sequence or parallel. "
    "Respond with a JSON array of actions, e.g.: "
    "[{\"tool\": \"TOOL1\", \"args\": {...}}, {\"prompt\": \"PROMPT2\", \"args\": {...}}]. "
    "You may chain results by referencing previous outputs."
)
class PromptsClient:
    """
    Client for rendering server-side prompts via FastMCP.
    """
    def __init__(self, mcp_client):
        self._mcp_client = mcp_client

    async def render(self, prompt_name, **kwargs):
        """
        Render a prompt by name with arguments.
        """
        return await self._mcp_client.render_prompt(prompt_name, kwargs)
