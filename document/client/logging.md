# client/logging.py

**Purpose:**
Client for logging events via FastMCP or locally.

**Key Entities:**
- LoggingClient: Wraps FastMCP logging methods.

**API:**
- log(message, level="info"): Logs a message to the server or locally. Uses FastMCP if available, else prints.
