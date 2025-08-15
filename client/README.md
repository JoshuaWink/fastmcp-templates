# Client — fastmcp-templates

This folder contains a modular MCP client built on top of a FastMCP client.

Highlights
- `client/client.py`: High-level `MCPClient` wrapper that composes subclients (tools, resources, prompts, notifications, logging, elicitation, discovery, subscriptions).
- `client/app/*`: Per-area helpers (tools, prompts, resources, discovery, subscribe/streaming logic).

Quick examples

1) Create a client from `mcp.json` in the repo root:

```py
from client.client import MCPClient

client = MCPClient()  # loads mcp.json from repo root
```

2) Call a tool

```py
result = await client.tools.call("echo_tool", {"message": "hello"})
```

3) Subscribe to a stream

```py
async for event in client.subscriptions.listen("demo_subscription"):
    print(event)
```

Notes
- The `SubscriptionClient` centralizes streaming/cancellation logic so production code remains test-free and clean.
- See tests in `tests/client` for usage patterns and expected behaviors.
