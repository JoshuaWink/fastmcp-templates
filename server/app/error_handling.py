
"""
Area of Responsibility: Error Handling
- Register error handling middleware or classes here.
- Standardize error responses and logging for all server endpoints.
- Document error schemas for LLM/agent and client use.
"""

def register_error_handlers(server):
    """
    Register error handling middleware or classes with the FastMCP server instance.
    """
    @server.error_handler("demo_error_handler", "Demo error handler")
    def demo_error_handler(exc, context=None):
        """
        Demo error handler that logs and returns a standard error response.
        Args:
            exc (Exception): The exception raised.
            context (dict, optional): Additional context.
        Returns:
            dict: Standardized error response.
        """
        print(f"[ERROR] {exc}")
        return {"error": str(exc), "type": type(exc).__name__}
