
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
    @server.tool(name="list_demo_capabilities", description="Lists registered demo capabilities.")
    def list_demo_capabilities() -> dict:
        """
        Demo discovery endpoint that lists registered demo capabilities.
        Returns:
            dict: Names of demo tools, resources, prompts, etc.
        """
        return {
            "tools": ["hello_tool"],
            "resources": ["hello_resource"],
            "prompts": ["hello_prompt"],
            "subscriptions": ["demo_subscription", "demo_notification"],
            "auth": ["demo_auth_provider"],
        }
