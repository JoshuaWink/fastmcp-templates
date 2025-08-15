class ResourcesClient:
    """
    Client for accessing server-exposed resources via FastMCP.
    """
    def __init__(self, fastmcp_client):
        self._client = fastmcp_client

    def get(self, resource_name):
        """
        Fetch a resource by name or URI.
        """
        return getattr(self._client.resources, resource_name)()
