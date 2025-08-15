class LoggingClient:
    """
    Client for logging events via FastMCP or locally.
    """
    def __init__(self, fastmcp_client):
        self._client = fastmcp_client

    def log(self, message, level="info"):
        """
        Log a message to the server or locally.
        """
        # If FastMCP supports logging, use it; else, print
        if hasattr(self._client, "log"):
            return self._client.log(message=message, level=level)
        print(f"[{level.upper()}] {message}")
