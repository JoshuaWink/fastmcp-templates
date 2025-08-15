# Areas of Responsibility

This document maps responsibilities across client, server, and platform teams.

- Client: UI integration, calling tools, handling notifications, and local caching.
- Server: Registering tools/resources/prompts, authentication, and long-running task handling.
- Platform: Deployment, CI, monitoring, and secrets management.

Example code (client-side helper):

```python
# Example: client helper
async def call_echo(client, message):
    return await client.tools.call("echo", {"message": message})
```