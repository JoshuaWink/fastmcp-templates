
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
    @server.auth_provider(name="demo_auth", description="Demo static token auth provider.")
    def demo_auth(token: str = None):
        if token == "demo-token":
            return {"user": "demo"}
        raise Exception("Invalid token")
