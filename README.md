
# fastmcp-templates

**A reference kit for building robust, modular Model Context Protocol (MCP) clients and servers with FastMCP.**

---

## Why fastmcp-templates?

This repo is for engineers and product teams who want:
- A clear, modular starting point for MCP client/server projects
- Best practices for context management (LLM, agent, or workflow)
- Side-by-side demos of config-driven (YAML) and self-documenting (modulink-py) context flows
- Annotated code, real-world patterns, and testable examples

---

## What's Inside

- `client/` — Modular MCP client with pluggable tools, resources, prompts, notifications, logging, elicitation, and discovery
- `server/` — Minimal, declarative FastMCP server with all business logic in `app/`
- `document/context_management_approaches.md` — Hands-on guide: config-driven vs. self-documenting context management
- `tests/` — Pytest suite for context, client, and server logic
- `document/` — Architecture, guides, and annotated flows

---

## Quickstart

1. **Clone the repo:**
	```sh
	git clone https://github.com/JoshuaWink/fastmcp-templates.git
	cd fastmcp-templates
	```
2. **Set up your environment:**
	```sh
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt  # or see pyproject.toml
	```
3. **Explore the code:**
	- Start with `client/client.py` and `server/server.py`
	- See `document/context_management_approaches.md` for context patterns
4. **Run the tests:**
	```sh
	pytest
	```

---

## Context Management: Two Approaches

See [`document/context_management_approaches.md`](document/context_management_approaches.md) for:
- **Config-driven (YAML):** Explicit, reorderable, non-dev friendly
- **Self-documenting chain:** Code-as-truth, always up to date, dev friendly

---

## When to Use This Repo

- Prototyping a new MCP client or server
- Teaching best practices for LLM/agent context flows
- Comparing config vs. code-driven context management
- Building production-ready, modular FastMCP apps

---

## License

Apache-2.0 — use, adapt, and share.
