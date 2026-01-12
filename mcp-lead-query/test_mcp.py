#!/usr/bin/env python3
"""
Quick MCP Server Test Script
Tests the MCP server functionality without full client setup
"""

import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_server import MCPLeadQueryServer

def test_mcp_server():
    """Test the MCP server directly"""
    print("🧪 Testing MCP Lead Query Server")
    print("=" * 40)
    
    server = MCPLeadQueryServer()
    
    # Test 1: List tools
    print("\n1️⃣ Testing tools/list")
    request = {"method": "tools/list", "params": {}}
    response = server.handle_request(request)
    
    if "tools" in response:
        tools = response["tools"]
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool['name']}: {tool['description']}")
    else:
        print("❌ Failed to get tools")
        return False
    
    # Test 2: Get lead stats
    print("\n2️⃣ Testing get_lead_stats")
    request = {
        "method": "tools/call",
        "params": {
            "name": "get_lead_stats",
            "arguments": {}
        }
    }
    response = server.handle_request(request)
    
    if "content" in response:
        print("✅ Stats retrieved:")
        for content in response["content"]:
            if content["type"] == "text":
                print(f"   {content['text']}")
    else:
        print("❌ Failed to get stats")
        return False
    
    # Test 3: Query leads
    test_questions = [
        "How many leads do we have?",
        "Show me all hot leads",
        "Any leads from Microsoft?"
    ]
    
    for i, question in enumerate(test_questions, 3):
        print(f"\n{i}️⃣ Testing query: '{question}'")
        request = {
            "method": "tools/call",
            "params": {
                "name": "query_leads",
                "arguments": {"question": question}
            }
        }
        response = server.handle_request(request)
        
        if "content" in response:
            print("✅ Query successful:")
            for content in response["content"]:
                if content["type"] == "text":
                    # Show first few lines of response
                    lines = content["text"].split('\n')
                    for line in lines[:3]:
                        if line.strip():
                            print(f"   {line}")
                    if len(lines) > 3:
                        print("   ...")
        else:
            print("❌ Query failed")
            return False
    
    print("\n🎉 All MCP server tests passed!")
    return True

if __name__ == "__main__":
    test_mcp_server()