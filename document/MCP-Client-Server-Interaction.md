# MCP Client-Server Interaction
# Supported Actors and Actions

MCP clients and servers support a range of actors and actions for flexible, event-driven workflows:

**Actors:**
- Client (human, program, or agent)
- Server (FastMCP server)
- LLM/Agent (optional, can act as client or server-side automation)
- User (end-user, often via a client UI)

**Actions:**
- **Tool Execution:** Call server-registered tools (functions) by name, passing parameters and receiving results.
- **Resource Access:** Fetch resources (files, data, objects) exposed by the server.
- **Prompt Rendering:** Request prompt templates or dynamic prompts from the server.
- **Logging:** Servers can send log messages to clients; clients can log events via tools.
- **Progress Reporting:** Servers can send progress updates to clients during long-running operations.
- **Elicitation:** Servers can request structured input from clients/users during tool execution.
- **Discovery:** Clients can list all available tools, resources, and prompts on the server.
- **Notifications:** Servers can send notifications to clients, which are queued by priority (e.g., low, medium, high, critical). Clients can review, clear, or defer notifications at their own pace, supporting both live alerts and persistent reminders. This enables workflows where important events are surfaced without disrupting the user's focus.

> Example: **7 notifications; 6 low-priority, 1 critical-priority**
>
> Clients can display, queue, and manage notifications, choosing when to address them. This pattern supports both immediate alerts and non-blocking reminders, improving user experience and workflow control.


## Overview
The MCP protocol defines how clients and servers communicate, enabling clients to discover and execute server-side tools, access resources, and render prompts.

## Data Flow
- **Startup:** Server registers tools/resources/prompts and starts listening.
- **Discovery:** Client lists available tools/resources/prompts.
- **Execution:** Client calls a tool or fetches a resource; server executes and returns the result.
- **Events:** Server can send logs, progress, or elicitation requests to the client.

## Example Workflow
1. Client connects to server.
2. Client lists available tools.
3. Client calls a tool (e.g., `log_event`).
4. Server executes the tool and returns the result.

## Example: End-to-End
```python
# Client
from fastmcp.client import Client
client = Client("http://localhost:8000")
print(client.tools.doc_tool())

# Server (tool definition)
@server.tool(name="doc_tool", description="Return documentation for all registered tools.")
def doc_tool():
    return str(server.list_tools())
```

## Example: mcp.json Configuration

The `mcp.json` file defines how a client connects to an MCP server, including transport, authentication, and roots. Place this file in your project root or pass its path to the client.

```json
{
    "servers": [
        {
            "name": "Local FastMCP Server",
            "url": "http://localhost:8000",
            "transport": "http",
            "auth": {
                "type": "bearer",
                "token": "YOUR_TOKEN_HERE"
            },
            "roots": ["."]
        }
    ]
}
```

## Troubleshooting
- Ensure server is running and accessible.
- Check authentication and transport settings.
- Use MCP Inspector for debugging and discovery.
