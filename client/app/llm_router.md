
# LLMRouter SDK Documentation

## Purpose
`LLMRouter` is an SDK designed for context engineers to orchestrate client-side context, tool routing, and prompt workflows in LLM-powered applications.

## Intended Audience
- **Context Engineers:** Those building and customizing context-aware workflows, toolchains, and agent orchestration for LLMs.
- **SDK/API Users:** Developers who need a pluggable, extensible interface for integrating LLM tool calls and prompt routing into their own code.

## Key Features
- **Extensible SDK:** Subclass or override methods to customize routing, chaining, and orchestration logic.
- **Unified Interface:** Route tool calls and prompt invocations to the appropriate LLM, agent, or workflow.
- **Integration:** Works seamlessly with `MCPClient` and other `client.app` modules for modular orchestration.


## Example Interface
```python
class LLMRouter:
    """
    Minimal dispatcher: routes a single tool, prompt, or resource call.
    Context engineers can extend or override methods for custom routing.
    """
    def __init__(self, client):
        self.client = client

    def route(self, message):
        """
        Routes a single tool, prompt, or resource call.
        Args:
            message (dict): {"tool": ..., "args": ...} or {"prompt": ...} or {"resource": ...}
        Returns:
            Any: Result from the appropriate client section.
        """
        if "tool" in message:
            return self.client.tools.call(message["tool"], **message.get("args", {}))
        if "prompt" in message:
            return self.client.prompts.render(message["prompt"], **message.get("args", {}))
        if "resource" in message:
            return self.client.resources.get(message["resource"])
        raise ValueError("Unknown message type")

    # Future: Batch/chain parsing and orchestration
    # def route_batch(self, messages):
    #     """
    #     Accepts a list of messages and executes them sequentially or in parallel.
    #     Useful for chaining tool calls, aggregating results, or feeding outputs into system prompts.
    #     """
    #     results = []
    #     for msg in messages:
    #         results.append(self.route(msg))
    #     return results
```

## Future Extensions
- **Batch/chain parsing:** Support for executing multiple tool/prompt/resource calls in sequence or parallel, enabling richer workflows and chaining results.
- **System prompt integration:** Feed results into a system prompt or use outputs as context for subsequent actions.

## Notes
- Replace this stub with a real implementation as needed for your project.
- This SDK is intended for direct use and extension by context engineers.
- Provides a starting point for LLM routing logic in the client.
