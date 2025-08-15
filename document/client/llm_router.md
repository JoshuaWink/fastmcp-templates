# client/llm_router.py

**Purpose:**
Routes LLM JSON tool/resource calls to the correct client method. Exposes available tools, prompts, and resources for LLM discovery.

**Key Entities:**
- LLMRouter: Main router class.
- format_for_llm: Utility to serialize dicts as compact JSON for LLM handoff.

**API:**
- get_llm_capabilities(): Returns compact JSON string of available tools, prompts, resources.
- route(llm_json_str): Accepts a JSON string from an LLM and routes to the correct tool/resource/prompt.

**Data Flow:**
- LLM outputs JSON tool/resource call → route() parses and dispatches.
- get_llm_capabilities() exposes available actions for LLM planning.
