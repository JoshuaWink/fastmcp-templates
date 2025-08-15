"""
MCP Client: Wraps the real FastMCP client and provides modular extensions for tools, resources, prompts, logging, progress, elicitation, discovery, and notifications (with priority queues).
"""

from fastmcp.client import Client as FastMCPClient
from client.app.tools import ToolsClient
from client.app.resources import ResourcesClient
from client.app.prompts import PromptsClient
from client.app.notifications import NotificationsClient
from client.app.logging import LoggingClient
from client.app.elicitation import ElicitationClient
from client.app.discovery import DiscoveryClient


class MCPClient:
    """
    High-level MCP Client wrapper.
    Provides modular access to tools, resources, prompts, notifications, logging, progress, elicitation, and discovery.
    Wraps the FastMCP client and can be extended for custom logic.
    """
    def __init__(self, config_or_path=None):
        """
        Args:
            config_or_path (dict or str): Dict config or path to mcp.json config file.
        """
        config = self._load_config(config_or_path)
        self._client = FastMCPClient(**config)
        self.tools = ToolsClient(self._client)
        self.resources = ResourcesClient(self._client)
        self.prompts = PromptsClient(self._client)
        self.notifications = NotificationsClient(self._client)
        self.logging = LoggingClient(self._client)
        self.elicitation = ElicitationClient(self._client)
        self.discovery = DiscoveryClient(self._client)

    @staticmethod
    def _load_config(config_or_path):
        """
        Load config from dict or JSON file path.
        """
        import os, json
        if config_or_path is None:
            # Try default mcp.json in cwd
            config_path = os.path.join(os.getcwd(), 'mcp.json')
            if os.path.exists(config_path):
                with open(config_path) as f:
                    return json.load(f)["servers"][0]
            raise ValueError("No config provided and mcp.json not found.")
        if isinstance(config_or_path, dict):
            return config_or_path
        if isinstance(config_or_path, str):
            with open(config_or_path) as f:
                return json.load(f)["servers"][0]
        raise TypeError("config_or_path must be dict or str (path to mcp.json)")

    def get_fastmcp_client(self):
        """
        Access the underlying FastMCP client for advanced usage.
        """
        return self._client
