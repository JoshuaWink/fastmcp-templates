
"""
Area of Responsibility: Prompts
- Register all @server.prompt-decorated functions here.
- Prompts provide reusable templates or logic for LLM/agent workflows.
- Document prompt schemas and usage for discoverability.
"""

def register_prompts(server):
    """
    Register all prompt templates or logic with the FastMCP server instance.
    """

    # Register hello_prompt as both a prompt and a tool
    def hello_prompt(name: str = "World") -> str:
        """
        Demo prompt that formats a greeting with a name argument.
        Args:
            name (str): Name to greet.
        Returns:
            str: Greeting message.
        """
        return f"Prompt says: Hello, {name}!"

    server.prompt(name="hello_prompt", description="Demo prompt that formats a greeting.")(hello_prompt)
    server.tool(name="hello_prompt", description="Tool wrapper for prompt 'hello_prompt'.")(hello_prompt)
