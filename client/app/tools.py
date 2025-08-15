class ToolsClient:
    """
    Client for executing server-registered tools via FastMCP.
    """
    def __init__(self, fastmcp_client):
        self._client = fastmcp_client

    def call(self, tool_name, **kwargs):
        """
        Call a tool by name with parameters.
        """
        return getattr(self._client.tools, tool_name)(**kwargs)
