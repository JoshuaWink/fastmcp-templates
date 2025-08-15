class ElicitationClient:
    """
    Client for handling elicitation (structured input requests) via FastMCP.
    """
    def __init__(self, fastmcp_client):
        self._client = fastmcp_client

    def request(self, schema, prompt=None):
        """
        Request structured input from the user or client.
        """
        # If FastMCP supports elicitation, use it; else, prompt
        if hasattr(self._client, "elicit"):
            return self._client.elicit(schema=schema, prompt=prompt)
        return input(prompt or str(schema))
