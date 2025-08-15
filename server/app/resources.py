
"""
Area of Responsibility: Resources
- Register all @server.resource-decorated functions here.
- Resources expose files, data, or live objects to agents/LLMs via MCP.
- Use absolute URIs and document resource schemas for discoverability.
"""

def register_resources(server):
    """
    Register all resources with the FastMCP server instance.
    """
    @server.resource(uri="resource://hello_resource", name="Hello Resource", description="Demo resource that returns a static string.")
    def hello_resource():
        """
        Demo resource that returns a static string.
        Returns:
            str: Demo resource content.
        """
        return "Hello from the resource!"
