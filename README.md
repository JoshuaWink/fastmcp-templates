
# fastmcp-templates

**A reference kit for building robust, modular Model Context Protocol (MCP) clients and servers with FastMCP.**

---

# fastmcp-templates

A reference kit for building robust, modular Model Context Protocol (MCP) clients and servers using FastMCP.

This repository is organized so teams can quickly bootstrap a client, a server, or explore the accompanying design documents and tests.

## Overview

- `client/` — MCP client implementation and helper subclients. See `client/README.md` for usage and examples.
- `server/` — FastMCP server template and example `app/` modules. See `server/README.md` for running and extending.
- `document/` — Architecture notes, guides, and comparison essays; `document/README.md` summarizes the docs.
- `tests/` — Pytest-based unit and integration tests that exercise client/server flows and subscriptions.

## Quickstart

1. Clone and enter the repo:

```sh
git clone https://github.com/JoshuaWink/fastmcp-templates.git
cd fastmcp-templates
```

2. Create and activate a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies (project uses pyproject.toml where possible):

```sh
pip install -r requirements.txt
```

4. Run the test suite:

```sh
pytest -q
```

5. Read the area docs:

- Client: `client/README.md`
- Server: `server/README.md`
- Docs: `document/README.md`

## Templates & Usage

This repo is marked as a GitHub template. Use the green "Use this template" button on GitHub to scaffold a new repo.

## Contributing

Please open issues or pull requests. Tests are required for new features.

## License

Apache-2.0
