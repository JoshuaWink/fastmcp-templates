# client/client.py

**Purpose:**
High-level MCP Client wrapper. Provides modular access to tools, resources, prompts, notifications, logging, progress, elicitation, and discovery. Wraps the FastMCP client and can be extended for custom logic.

**Key Entities:**
- MCPClient: Main entry point, instantiates all subclients.
- Subclients: ToolsClient, ResourcesClient, PromptsClient, NotificationsClient, LoggingClient, ProgressClient, ElicitationClient, DiscoveryClient.

**Data Flow:**
- Loads config (dict or path).
- Instantiates FastMCPClient.
- Attaches subclients for each domain.

**Relationships:**
- Each subclient wraps a domain-specific part of the FastMCP client.
- All business logic is delegated to subclients.
