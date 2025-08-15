
"""
Area of Responsibility: Authentication/Session
- Register authentication providers or session logic here.
- Supports OAuth, tokens, or custom auth patterns.
- Document auth/session schemas for discoverability and security.
"""

def register_auth(server):
    """
    Register authentication providers or session logic with the FastMCP server instance.
    """
    @server.auth(
        name="demo_auth_provider",
        description="Demo in-memory authentication provider."
    )
    def demo_auth_provider(username: str, password: str) -> bool:
        """
        Demo in-memory authentication provider.
        Args:
            username (str): Username.
            password (str): Password.
        Returns:
            bool: True if credentials match demo user, else False.
        """
        return username == "demo_user" and password == "password123"
