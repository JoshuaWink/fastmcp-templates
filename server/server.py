# Entrypoint for FastMCP server
from mcp.server.fastmcp.server import FastMCP as BaseFastMCP

from app.tools import register_tools
from app.resources import register_resources
from app.prompts import register_prompts
from app.subscriptions import register_subscriptions
# from app.notifications import register_notifications
from app.auth import register_auth
from app.discovery import register_discovery
# from app.error_handling import register_error_handlers
from app.schema import register_schema



class FastMCP(BaseFastMCP):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._subscriptions = {}
        self._auth_providers = {}

    def subscription(self, name=None, description=None):
        def decorator(fn):
            reg_name = name or fn.__name__
            self._subscriptions[reg_name] = {
                "handler": fn,
                "description": description or fn.__doc__
            }
            return fn
        return decorator

    def auth_provider(self, name=None, description=None):
        def decorator(fn):
            reg_name = name or fn.__name__
            self._auth_providers[reg_name] = {
                "handler": fn,
                "description": description or fn.__doc__
            }
            return fn
        return decorator

server = FastMCP(name="My MCP Server")
register_tools(server)
register_resources(server)
register_prompts(server)
register_subscriptions(server)
# register_notifications(server)
register_auth(server)
register_discovery(server)
# register_error_handlers(server)
register_schema(server)

if __name__ == "__main__":
    server.run(transport="stdio")
