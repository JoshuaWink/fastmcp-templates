import subprocess
import pytest
import subprocess
import time
import os
import sys
import asyncio
import signal
from client.client import MCPClient

MCP_CONFIG_PATH = "tests/integration/mcp.json"

@pytest.fixture(scope="module")
def mcp_server():
    env = os.environ.copy()
    venv_site = '/Users/joshuawink/Documents/github/fastmcp-templates/.venv/lib/python3.13/site-packages'
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    env['PYTHONPATH'] = f"{venv_site}:{project_root}"
    env['PATH'] = f"/Users/joshuawink/Documents/github/fastmcp-templates/.venv/bin:" + env.get('PATH', '')
    proc = subprocess.Popen([
        sys.executable, "server/server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=project_root, env=env)
    time.sleep(2)
    yield proc
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()

@pytest.mark.asyncio
async def test_handshake(mcp_server):
    from client.client import MCPClient
    client = MCPClient(MCP_CONFIG_PATH)
    async with client._client:
        tools = await client.discovery.list_tools()
        assert isinstance(tools, list)
