class DiscoveryClient:
    """
    Client for discovering tools, resources, and prompts via FastMCP.
    """
    def __init__(self, fastmcp_client):
        self._client = fastmcp_client

    def list_tools(self):
        return self._client.tools.list()

    def list_resources(self):
        return self._client.resources.list()

    def list_prompts(self):
        return self._client.prompts.list()
