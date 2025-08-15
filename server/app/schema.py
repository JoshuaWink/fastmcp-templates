
"""
Area of Responsibility: Schema Exposure
- Register logic to expose OpenAPI/JSON schemas for all server entities.
- Enables LLM/agent and client-side schema discovery.
- Document schema endpoints for integration and validation.
"""

def register_schema(server):
    """
    Register schema exposure logic with the FastMCP server instance.
    """
    @server.resource(
        uri="schema://hello_tool",
        name="Hello Tool Schema",
        description="JSON schema for hello_tool."
    )
    def hello_tool_schema() -> dict:
        """
        Demo schema endpoint that exposes the JSON schema for hello_tool.
        Returns:
            dict: JSON schema for hello_tool.
        """
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name to greet."}
            },
            "required": [],
        }
