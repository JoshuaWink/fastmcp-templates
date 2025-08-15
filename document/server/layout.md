# Server Layout

A recommended layout for an MCP server project:

```
server/
  server.py          # Entrypoint
  app/
    tools.py
    resources.py
    prompts.py
    subscriptions.py
```

Keep `server.py` minimal; put business logic in `app/` modules.
