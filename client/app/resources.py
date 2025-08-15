class ResourcesClient:
    """
    Client for accessing server-exposed resources via FastMCP.
    """
    def __init__(self, fastmcp_client):
        self._client = fastmcp_client

    async def get(self, resource_name):
        """
        Fetch a resource by name or URI.
        """
        return await self._client.read_resource(resource_name)

    async def list(self):
        """
        List available resources (with metadata).
        """
        return await self._client.list_resources()
