# Entrypoint for FastMCP server
from mcp.server.fastmcp.server import FastMCP
from app.tools import register_tools
from app.resources import register_resources
from app.prompts import register_prompts
from app.subscriptions import register_subscriptions
from app.notifications import register_notifications
from app.auth import register_auth
from app.discovery import register_discovery
from app.error_handling import register_error_handling
from app.schema import register_schema

server = FastMCP(name="My MCP Server")
register_tools(server)
register_resources(server)
register_prompts(server)
register_subscriptions(server)
register_notifications(server)
register_auth(server)
register_discovery(server)
register_error_handling(server)
register_schema(server)

if __name__ == "__main__":
    server.run(transport="stdio")
