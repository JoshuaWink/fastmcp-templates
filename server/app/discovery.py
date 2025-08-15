
"""
Area of Responsibility: Discovery
- Register discovery logic for tools, resources, prompts, and subscriptions.
- Enables LLM/agent discoverability of all server capabilities.
- Document discovery endpoints and schemas for agent use.
"""

def register_discovery(server):
    """
    Register discovery logic with the FastMCP server instance.
    """
    @server.tool(name="list_demo_capabilities", description="Lists all registered capabilities.")
    def list_demo_capabilities() -> dict:
        """
        Lists all registered tools, resources, prompts, subscriptions, and auth providers.
        """
        tools = list(getattr(server, '_tools', {}).keys())
        resources = list(getattr(server, '_resources', {}).keys())
        prompts = list(getattr(server, '_prompts', {}).keys())
        subscriptions = list(getattr(server, '_subscriptions', {}).keys()) if hasattr(server, '_subscriptions') else []
        auth = list(getattr(server, '_auth_providers', {}).keys()) if hasattr(server, '_auth_providers') else []
        return {
            "tools": tools,
            "resources": resources,
            "prompts": prompts,
            "subscriptions": subscriptions,
            "auth": auth,
        }
