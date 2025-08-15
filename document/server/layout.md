# MCP Server Directory & Module Layout

This document maps out the recommended directory and module structure for a fully spec-compliant MCP server, with brief descriptions for each part. Use this as a reference for implementation and onboarding.

---

```
server/
  server.py                # Entrypoint: instantiates and runs the FastMCP server
  app/
    tools.py               # Define and register all server-side tools
    resources.py           # Define and register all resources (files, data, etc.)
    prompts.py             # Define and register prompt templates/logic
    subscriptions.py       # Define and register subscription topics/streams
    notifications.py       # (Optional) Notification schemas/logic (as a subscription extension)
    auth.py                # Authentication/session logic (OAuth, tokens, etc.)
    discovery.py           # Discovery logic for tools/resources/prompts/subscriptions
    error_handling.py      # Standardized error classes and middleware
    schema.py              # Expose OpenAPI/JSON schemas for all entities
    __init__.py
  document/
    ...                    # Mirrors app/ for documentation and schema
  REFERENCE.md             # Architecture reference and onboarding
  README.md                # Project overview and usage
  pyproject.toml           # Packaging and dependencies
```

---

**Descriptions:**
- `server.py`: Minimal entrypoint, registers and runs everything.
- `app/tools.py`: All callable tools (functions) for LLM/agent use.
- `app/resources.py`: All resources (files, APIs, DBs) exposed to clients.
- `app/prompts.py`: Prompt templates or logic for LLM workflows.
- `app/subscriptions.py`: Topics/streams for real-time updates (progress, logs, notifications).
- `app/notifications.py`: Notification schemas/logic (as a subscription extension).
- `app/auth.py`: Authentication/session management.
- `app/discovery.py`: Lists all registered tools/resources/prompts/subscriptions.
- `app/error_handling.py`: Error classes and middleware for robust error reporting.
- `app/schema.py`: Exposes OpenAPI/JSON schemas for all entities.
- `document/`: Mirrors `app/` for maintainable docs and schemas.
- `REFERENCE.md`, `README.md`: High-level docs and onboarding.
- `pyproject.toml`: Python packaging and dependencies.

---

**Testing:**
- Each module should have corresponding tests (e.g., `tests/app/test_tools.py`) focused on input/output only.
- Tests should validate registration, discovery, and correct input/output for each entity.
