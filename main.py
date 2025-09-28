# main.py

import os
import sys
import platform
from dotenv import load_dotenv
from mcp.server.stdio import stdio_server
import anyio
from logger import info, success, debug, log_startup_header, log_env_check, divider

# Load environment variables
load_dotenv()
info("🏗️  Initializing Odoo MCP Server...")

from server import mcp 

async def run_mcp_server():
    # Log environment variables
    env_vars = {
        "ODOO_URL": os.environ.get("ODOO_URL", ""),
        "ODOO_DB": os.environ.get("ODOO_DB", ""),
        "ODOO_USERNAME": os.environ.get("ODOO_USERNAME", ""),
        "ODOO_PASSWORD": os.environ.get("ODOO_PASSWORD", ""),
        "ODOO_PORT": os.environ.get("ODOO_PORT", ""),
        "ODOO_PROTOCOL": os.environ.get("ODOO_PROTOCOL", "")
    }

    # Log startup information
    log_startup_header()
    log_env_check(env_vars)

    info("🔌 Launching Odoo MCP server via stdio...")
    async with stdio_server() as (reader, writer):
        success("✅ MCP server lifespan context initialized")
        info("📡 MCP stdio connection established")
        info("🔄 Starting MCP server main loop...")
        await mcp._mcp_server.run(reader, writer, mcp._mcp_server.create_initialization_options())

def main():
    anyio.run(run_mcp_server)

if __name__ == "__main__":
    sys.exit(main())
