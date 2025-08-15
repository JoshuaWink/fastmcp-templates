class DiscoveryClient:
    """
    Client for discovering tools, resources, and prompts via FastMCP.
    """
    def __init__(self, fastmcp_client):
        self._client = fastmcp_client

    async def list_tools(self):
        return await self._client.list_tools()

    async def list_resources(self):
        return await self._client.list_resources()

    async def list_prompts(self):
        return await self._client.list_prompts()
