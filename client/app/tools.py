class ToolsClient:
    """
    Client for executing server-registered tools via FastMCP.
    """
    def __init__(self, fastmcp_client):
        self._client = fastmcp_client

    async def call(self, tool_name, **kwargs):
        """
        Call a tool by name with parameters.
        """
        return await self._client.call_tool(tool_name, kwargs)

    async def list(self):
        """
        List available tools (with metadata).
        """
        return await self._client.list_tools()
