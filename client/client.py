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
        self._client = FastMCPClient(config)
        self.tools = ToolsClient(self._client)
        self.resources = ResourcesClient(self._client)
        self.prompts = PromptsClient(self)
        self.notifications = NotificationsClient(self._client)
        self.logging = LoggingClient(self._client)
        self.elicitation = ElicitationClient(self._client)
        self.discovery = DiscoveryClient(self._client)
        from client.app.subscribe import SubscriptionClient
        self.subscriptions = SubscriptionClient(self)

    async def render_prompt(self, prompt_name, kwargs):
        """
        Render a prompt by calling the prompt as a tool (if supported by the server).
        Args:
            prompt_name (str): The name of the prompt to render.
            kwargs (dict): Arguments for the prompt.
        Returns:
            Any: The rendered prompt result.
        """
        # Many FastMCP servers expose prompts as tools with the same name
        return await self._client.call_tool(prompt_name, kwargs)

    @staticmethod
    def _load_config(config_or_path, server_name=None):
        """
        Loads and normalizes the config for FastMCPClient.
        Accepts a dict or a path to a JSON/YAML config file.
        Passes the config as-is (with 'mcpServers') to FastMCPClient.
        """
        import os, json, yaml
        if config_or_path is None:
            config_path = os.path.join(os.getcwd(), 'mcp.json')
            if os.path.exists(config_path):
                with open(config_path) as f:
                    config = json.load(f)
            else:
                raise ValueError("No config provided and mcp.json not found.")
        elif isinstance(config_or_path, str):
            ext = os.path.splitext(config_or_path)[1]
            with open(config_or_path, "r") as f:
                if ext in (".yaml", ".yml"):
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
        elif isinstance(config_or_path, dict):
            config = config_or_path
        else:
            raise ValueError("Config must be dict or path")

        # Always pass the config as-is (with 'mcpServers') to FastMCPClient
        if "mcpServers" in config:
            print("[DEBUG] Passing config to FastMCPClient:", config)
            return config
        elif "servers" in config:
            # For legacy support, convert 'servers' to 'mcpServers'
            config["mcpServers"] = config.pop("servers")
            print("[DEBUG] Passing config to FastMCPClient:", config)
            return config
        else:
            raise ValueError("Config must contain 'mcpServers' or 'servers'")
