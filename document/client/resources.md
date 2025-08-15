# client/resources.py

**Purpose:**
Client for accessing server-exposed resources via FastMCP.

**Key Entities:**
- ResourcesClient: Wraps FastMCP resource methods.

**API:**
- get(resource_name): Fetches a resource by name or URI.

**Architectural Note:**
Resources have their own expectations for data retrieval and structure (e.g., file contents, database records, or static data). Clients should handle resource types and formats appropriately for downstream use.
