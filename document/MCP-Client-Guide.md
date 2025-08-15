# MCP Client Guide

## What is an MCP Client?
An MCP client is a program or library that connects to an MCP server, discovers available tools, resources, and prompts, and executes them via the MCP protocol.

## Connecting to a Server
- Use the FastMCP client library or CLI to connect to a running MCP server.
- Configure authentication if required (e.g., Bearer token, OAuth).

## Discovering Tools, Resources, and Prompts
- Clients can list all registered tools, resources, and prompts exposed by the server.
- Each tool/resource/prompt has a name, description, and schema for arguments and results.

## Calling Tools and Resources
- Call tools by name, passing parameters or a payload dict.
- Fetch resources by URI or name.
- Render prompts with arguments.

## Example: Minimal Client Usage
```python
from fastmcp.client import Client
client = Client("http://localhost:8000")
result = client.tools.log_event(event="Started", payload={"foo": "bar"})
print(result)
```

## Authentication and Configuration
- Configure authentication as required by the server (see server docs).
- Set transport (stdio, HTTP, etc.) as needed.
