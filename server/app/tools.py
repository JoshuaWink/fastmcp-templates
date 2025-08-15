
"""
Area of Responsibility: Tools
- Register all @server.tool-decorated functions here.
- Tools expose callable automation, scripting, or API logic to agents/LLMs via MCP.
- Document tool schemas and usage for discoverability.
"""

def register_tools(server):
    """
    Register all server-side tools with the FastMCP server instance.
    """
    @server.tool(name="hello_tool", description="Demo tool that returns a greeting.")
    def hello_tool(name: str = "World") -> str:
        """
        Demo tool that returns a greeting.
        Args:
            name (str): Name to greet.
        Returns:
            str: Greeting message.
        """
        return f"Hello, {name}!"
