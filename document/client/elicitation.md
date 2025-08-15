# client/elicitation.py

**Purpose:**
Client for handling elicitation (structured input requests) via FastMCP.

**Key Entities:**
- ElicitationClient: Wraps FastMCP elicitation methods.

**API:**
- request(schema, prompt=None): Requests structured input from the user or client. Uses FastMCP if available, else falls back to input().
