# client/prompts.py

**Purpose:**
Client for rendering server-side prompts via FastMCP and for instructing LLMs to respond in JSON for tool/resource calls.

**Key Entities:**
- PromptsClient: Renders prompts by name.
- LLM_JSON_TOOL_CALL_PROMPT: Template for instructing LLMs to respond in JSON for tool/resource calls.

**API:**
- render(prompt_name, **kwargs): Renders a prompt by name with arguments.

**Annotations:**
- See top of file for context flow and tool call cycle notes for future context manager integration.

**Architectural Note:**
Prompts are technically a subtype of tool, but are expected to always return a specific string (template or message), not arbitrary data. This distinction is important for LLM workflows and UI rendering.
