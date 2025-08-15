import json

def format_for_llm(data):
    """
    Serialize a Python dict as a compact JSON string for LLM handoff.
    """
    import json
    return json.dumps(data, separators=(",", ":"))

class LLMRouter:
    """
    SDK/API-style stub for LLMRouter. Users can extend or override methods for custom routing.
    - Route tool calls and prompt invocations to the appropriate LLM or agent.
    - Provide a unified interface for LLM-based workflows (e.g., tool selection, prompt chaining, response parsing).
    - Integrate with MCPClient and other client.app modules for seamless orchestration.
    """
    def __init__(self, client):
        self.client = client

    def route(self, message):
        """
        Routes a single tool, prompt, or resource call.
        Args:
            message (dict or str): {"tool": ..., "args": ...} or {"prompt": ...} or {"resource": ...}, or JSON string.
        Returns:
            Any: Result from the appropriate client section.
        """
        if isinstance(message, str):
            message = json.loads(message)
        if "tool" in message:
            return self.client.tools.call(message["tool"], **message.get("args", {}))
        if "prompt" in message:
            return self.client.prompts.render(message["prompt"], **message.get("args", {}))
        if "resource" in message:
            return self.client.resources.get(message["resource"])
        raise ValueError("Unknown message type")

    def route_batch(self, messages, parallel=False):
        """
        Accepts a list of messages and executes them sequentially (default) or in parallel.
        Useful for chaining tool calls, aggregating results, or feeding outputs into system prompts.
        Args:
            messages (list): List of message dicts.
            parallel (bool): If True, execute in parallel (experimental/advanced).
        Returns:
            list: Results from each message.
        """
        if not messages:
            return []
        if parallel:
            # Experimental: naive parallel execution (no concurrency control)
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(executor.map(self.route, messages))
            return results
        else:
            # Sequential execution (default, safest for most models)
            results = []
            for msg in messages:
                results.append(self.route(msg))
            return results


    def get_llm_capabilities(self):
        """
        Returns a compact JSON string of available tools, prompts, and resources for LLM planning.
        """
        caps = {
            "tools": self.client.discovery.list_tools(),
            "prompts": self.client.discovery.list_prompts(),
            "resources": self.client.discovery.list_resources(),
        }
        return format_for_llm(caps)

    # (Removed duplicate route method for JSON string; unified above)
