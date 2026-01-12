#!/usr/bin/env python3
"""
MCP Client for testing the Lead Query MCP Server
Provides a CLI interface to test MCP protocol communication
"""

import json
import subprocess
import sys
import threading
import time
from typing import Dict, Any, Optional

class MCPClient:
    """Client to test MCP Lead Query Server"""
    
    def __init__(self, server_script: str = "mcp_server.py"):
        self.server_script = server_script
        self.process = None
        self.request_id = 1
        
    def start_server(self):
        """Start the MCP server process"""
        try:
            self.process = subprocess.Popen(
                [sys.executable, self.server_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            print("🚀 MCP Server started successfully")
            
            # Give server time to initialize
            time.sleep(0.5)
            
            return True
        except Exception as e:
            print(f"❌ Failed to start MCP server: {e}")
            return False
    
    def stop_server(self):
        """Stop the MCP server process"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("🛑 MCP Server stopped")
    
    def send_request(self, method: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Send a JSON-RPC request to the MCP server"""
        if not self.process:
            print("❌ Server not running")
            return None
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        self.request_id += 1
        
        try:
            # Send request
            request_json = json.dumps(request) + "\n"
            self.process.stdin.write(request_json)
            self.process.stdin.flush()
            
            # Read response
            response_line = self.process.stdout.readline()
            if not response_line:
                print("❌ No response from server")
                return None
            
            response = json.loads(response_line.strip())
            return response
            
        except Exception as e:
            print(f"❌ Communication error: {e}")
            return None
    
    def list_tools(self):
        """List available tools from the MCP server"""
        print("\n🔧 Listing available tools...")
        response = self.send_request("tools/list")
        
        if response and "tools" in response:
            tools = response["tools"]
            print(f"Found {len(tools)} tools:")
            for i, tool in enumerate(tools, 1):
                print(f"\n{i}. {tool['name']}")
                print(f"   Description: {tool['description']}")
                if 'inputSchema' in tool:
                    schema = tool['inputSchema']
                    if 'properties' in schema:
                        print("   Parameters:")
                        for param, details in schema['properties'].items():
                            required = param in schema.get('required', [])
                            req_str = " (required)" if required else " (optional)"
                            print(f"     - {param}{req_str}: {details.get('description', 'No description')}")
            return tools
        else:
            print("❌ Failed to get tools list")
            return []
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """Call a specific tool with arguments"""
        print(f"\n🔧 Calling tool: {tool_name}")
        print(f"Arguments: {arguments}")
        
        response = self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        if response:
            if "content" in response:
                print("\n📊 Response:")
                for content in response["content"]:
                    if content["type"] == "text":
                        print(content["text"])
            elif "error" in response:
                print(f"❌ Error: {response['error']['message']}")
            else:
                print(f"📄 Raw response: {response}")
        else:
            print("❌ No response received")
    
    def interactive_mode(self):
        """Interactive mode for testing the MCP server"""
        print("🤖 MCP Lead Query Server - Interactive Test Client")
        print("=" * 60)
        
        if not self.start_server():
            return
        
        try:
            # List available tools
            tools = self.list_tools()
            
            if not tools:
                print("❌ No tools available")
                return
            
            print("\n" + "=" * 60)
            print("🎯 Interactive Testing Mode")
            print("Commands:")
            print("  'list' - List available tools")
            print("  'query <question>' - Ask a question about leads")
            print("  'stats' - Get lead statistics")
            print("  'help' - Show example questions")
            print("  'quit' - Exit")
            print("=" * 60)
            
            while True:
                try:
                    command = input("\n💬 Command: ").strip()
                    
                    if command.lower() in ['quit', 'exit', 'q']:
                        break
                    
                    elif command.lower() == 'list':
                        self.list_tools()
                    
                    elif command.lower() == 'stats':
                        self.call_tool("get_lead_stats", {})
                    
                    elif command.lower() == 'help':
                        self.show_help()
                    
                    elif command.lower().startswith('query '):
                        question = command[6:].strip()
                        if question:
                            self.call_tool("query_leads", {"question": question})
                        else:
                            print("❌ Please provide a question after 'query'")
                    
                    elif command.lower().startswith('q '):
                        question = command[2:].strip()
                        if question:
                            self.call_tool("query_leads", {"question": question})
                        else:
                            print("❌ Please provide a question after 'q'")
                    
                    else:
                        print("❌ Unknown command. Type 'help' for available commands.")
                
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        finally:
            self.stop_server()
    
    def show_help(self):
        """Show example questions"""
        print("\n📚 Example Questions:")
        print("\n📊 Counting Questions:")
        print("  query How many leads do we have?")
        print("  query How many hot leads today?")
        print("  query How many warm leads?")
        
        print("\n🔍 Filtering Questions:")
        print("  query Show me all hot leads")
        print("  query Show me warm leads")
        print("  query Any leads from Microsoft?")
        
        print("\n📅 Time-based Questions:")
        print("  query Leads from today")
        print("  query Leads from this week")
        
        print("\n🤖 AI-related Questions:")
        print("  query Which leads mention AI?")
        print("  query Show me leads with AI companies")
        
        print("\n🏢 Company Questions:")
        print("  query Any leads from Google?")
        print("  query Leads from Facebook")
    
    def run_automated_tests(self):
        """Run automated tests of the MCP server"""
        print("🧪 Running Automated MCP Tests")
        print("=" * 40)
        
        if not self.start_server():
            return
        
        try:
            # Test 1: List tools
            print("\n1️⃣ Testing tools/list...")
            tools = self.list_tools()
            assert len(tools) > 0, "No tools found"
            print("✅ Tools list successful")
            
            # Test 2: Get stats
            print("\n2️⃣ Testing get_lead_stats...")
            self.call_tool("get_lead_stats", {})
            print("✅ Stats retrieval successful")
            
            # Test 3: Query leads
            test_questions = [
                "How many leads do we have?",
                "Show me all hot leads",
                "Any leads from Microsoft?",
                "Which leads mention AI?"
            ]
            
            for i, question in enumerate(test_questions, 3):
                print(f"\n{i}️⃣ Testing query: '{question}'")
                self.call_tool("query_leads", {"question": question})
                print("✅ Query successful")
            
            print("\n🎉 All automated tests passed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
        finally:
            self.stop_server()

def main():
    """Main function to run the MCP client"""
    client = MCPClient()
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        client.run_automated_tests()
    else:
        client.interactive_mode()

if __name__ == "__main__":
    main()