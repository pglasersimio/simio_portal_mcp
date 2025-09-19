# server.py
from helpers import log
from mcp_app import mcp  # the shared FastMCP instance
import api_tools_rest_generated
import tools  # importing registers all @mcp.tool()s
import workflow_tools

if __name__ == "__main__":
    log.info("Starting SimioPortalTools...")
    mcp.run()
