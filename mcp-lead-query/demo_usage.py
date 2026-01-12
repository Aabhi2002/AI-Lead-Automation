#!/usr/bin/env python3
"""
Demo script showing how to use the MCP Lead Query CLI
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_cli_test import MCPTestCLI

def main():
    """Demo the MCP CLI usage"""
    print("🎯 MCP Lead Query CLI - Usage Demo")
    print("=" * 50)
    
    cli = MCPTestCLI()
    
    print("\n✅ The CLI now accepts questions in multiple ways:")
    print()
    
    # Show different ways to ask the same question
    demo_examples = [
        ("Direct question", "How many hot leads?"),
        ("With 'query' prefix", "query How many hot leads?"),
        ("With 'q' prefix", "q How many hot leads?"),
    ]
    
    print("🔍 Different ways to ask the same question:")
    for method, example in demo_examples:
        print(f"   {method}: '{example}'")
    
    print("\n📝 Try these questions directly in the CLI:")
    example_questions = [
        "Give me all warm leads",
        "How many hot leads?", 
        "Any leads from Microsoft?",
        "Show me cold leads",
        "Which leads mention AI?",
        "Leads from Facebook",
        "How many leads do we have?"
    ]
    
    for question in example_questions:
        print(f"   • {question}")
    
    print("\n🚀 Start the interactive CLI:")
    print("   python3 mcp-lead-query/mcp_cli_test.py")
    
    print("\n💡 In the CLI, you can type:")
    print("   🎯 Command: How many hot leads?")
    print("   🎯 Command: Give me all warm leads")
    print("   🎯 Command: stats")
    print("   🎯 Command: help")
    print("   🎯 Command: quit")
    
    print("\n" + "=" * 50)
    print("✨ Your MCP Lead Query Agent is ready to use!")

if __name__ == "__main__":
    main()