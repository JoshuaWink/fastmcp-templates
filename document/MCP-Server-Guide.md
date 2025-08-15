# MCP Server Guide

## What is an MCP Server?
A Model Context Protocol (MCP) server exposes automation, scripting, or API logic to clients and LLMs. It registers callable tools, resources, and prompts, making them discoverable and executable via the MCP protocol.

## Directory Structure
- `<lib>-mcp-server/`
  - `server.py`: Entrypoint. Instantiates the FastMCP server, registers all tools/resources/prompts, and starts the server.
  - `app/`: All business logic lives here.
    - `tools.py`: Define and register callable tools.
    - `resources.py`: (Optional) Register shared resources.
    - `prompts.py`: (Optional) Register prompt templates or logic.
  - `REFERENCE.md`, `README.md`: Documentation.
  - `pyproject.toml`, `build/`, `<lib>_mcp_server.egg-info/`: Packaging and build artifacts.

## Entrypoint Example
```python
from mcp.server.fastmcp.server import FastMCP
from app.tools import register_tools
from app.resources import register_resources
from app.prompts import register_prompts

server = FastMCP(name="VSCode CLI MCP Server")
register_tools(server)
register_resources(server)
register_prompts(server)

if __name__ == "__main__":
    server.run(transport="stdio")
```

## Defining Tools, Resources, and Prompts
- **Tools:** Python functions decorated with `@server.tool`, registered in `register_tools(server)`.
- **Resources:** Data or objects exposed with `@server.resource`, registered in `register_resources(server)`.
- **Prompts:** Templates or logic with `@server.prompt`, registered in `register_prompts(server)`.

## Extending the Server
- Add new tools/resources/prompts by defining and registering them in `app/`.
- Keep `server.py` minimal and declarative.
- Use the MCP Inspector or client to discover all tools, resources, and prompts.

## Example: Adding a Tool
```python
@server.tool(name="log_event", description="Log an event or annotation.")
def log_event(event: str, payload: dict = None):
    with open("server.log", "a") as f:
        f.write(f"{event}: {json.dumps(payload)}\n")
    return "Logged."
# Register in register_tools(server)
```
