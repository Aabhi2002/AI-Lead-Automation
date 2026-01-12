#!/usr/bin/env python3
"""
Quick start script for MCP Lead Query CLI
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_cli_test import MCPTestCLI

def main():
    """Start the MCP CLI"""
    print("🚀 Starting MCP Lead Query CLI...")
    print()
    
    cli = MCPTestCLI()
    cli.interactive_mode()

if __name__ == "__main__":
    main()