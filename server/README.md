# Server — fastmcp-templates

This folder contains a minimal FastMCP-compatible server scaffold with modular `app/` modules.

Highlights
- `server/server.py`: Entrypoint — instantiates the FastMCP server, registers tools/resources/prompts/subscriptions, and runs the server.
- `server/app/*`: Business logic lives here (auth, discovery, tools, prompts, subscriptions, error handling).

Quick run (development)

```sh
python server/server.py
```

Testing

- See `tests/server` for unit tests that exercise registration, decorator behavior, and subscription generators.

Extending

- Add new tools via `@server.tool` in `server/app/tools.py` and register in `server/server.py`.
- Add resources with `@server.resource`, prompts with `@server.prompt`, and subscriptions with `@server.subscription`.
