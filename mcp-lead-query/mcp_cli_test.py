#!/usr/bin/env python3
"""
Simple CLI interface to test MCP Lead Query functionality
Direct integration without subprocess complexity
"""

import sys
import os
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_server import MCPLeadQueryServer

class MCPTestCLI:
    """Simple CLI to test MCP functionality"""
    
    def __init__(self):
        self.server = MCPLeadQueryServer()
        self.request_id = 1
    
    def send_request(self, method: str, params: dict = None):
        """Send a request to the MCP server"""
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        self.request_id += 1
        
        response = self.server.handle_request(request)
        response["id"] = request["id"]
        response["jsonrpc"] = "2.0"
        
        return response
    
    def list_tools(self):
        """List available MCP tools"""
        print("\n🔧 Available MCP Tools:")
        print("-" * 40)
        
        response = self.send_request("tools/list")
        
        if "tools" in response:
            for i, tool in enumerate(response["tools"], 1):
                print(f"{i}. {tool['name']}")
                print(f"   📝 {tool['description']}")
                
                if 'inputSchema' in tool and 'properties' in tool['inputSchema']:
                    print("   📋 Parameters:")
                    schema = tool['inputSchema']
                    for param, details in schema['properties'].items():
                        required = param in schema.get('required', [])
                        req_str = " (required)" if required else ""
                        print(f"      • {param}{req_str}: {details.get('description', 'No description')}")
                print()
        else:
            print("❌ No tools available")
    
    def call_tool(self, tool_name: str, arguments: dict):
        """Call an MCP tool"""
        print(f"\n🔧 Calling: {tool_name}")
        if arguments:
            print(f"📝 Arguments: {arguments}")
        print("-" * 50)
        
        response = self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        if "content" in response:
            for content in response["content"]:
                if content["type"] == "text":
                    print(content["text"])
        elif "error" in response:
            print(f"❌ Error: {response['error']['message']}")
        else:
            print(f"📄 Response: {json.dumps(response, indent=2)}")
    
    def run_demo(self):
        """Run a demonstration of MCP capabilities"""
        print("🤖 MCP Lead Query Server - Demo Mode")
        print("=" * 60)
        
        # List tools
        self.list_tools()
        
        print("🎯 Demo Queries:")
        print("=" * 30)
        
        # Demo queries
        demo_queries = [
            ("get_lead_stats", {}, "Get overall lead statistics"),
            ("query_leads", {"question": "How many leads do we have?"}, "Count all leads"),
            ("query_leads", {"question": "Show me all hot leads"}, "List hot leads"),
            ("query_leads", {"question": "Any leads from Microsoft?"}, "Find Microsoft leads"),
            ("query_leads", {"question": "Which leads mention AI?"}, "Find AI-interested leads"),
        ]
        
        for i, (tool, args, description) in enumerate(demo_queries, 1):
            print(f"\n{i}. {description}")
            self.call_tool(tool, args)
            print()
    
    def interactive_mode(self):
        """Interactive mode for testing"""
        print("🤖 MCP Lead Query Server - Interactive Test Mode")
        print("=" * 60)
        
        self.list_tools()
        
        print("\n💬 Commands:")
        print("  stats                    - Get lead statistics")
        print("  query <question>         - Ask about leads")
        print("  q <question>             - Short form query")
        print("  demo                     - Run demonstration")
        print("  help                     - Show example questions")
        print("  quit                     - Exit")
        print("\n💡 Tip: You can also ask questions directly!")
        print("     Just type: 'How many hot leads?' or 'Show me warm leads'")
        print("=" * 60)
        
        while True:
            try:
                command = input("\n🎯 Command: ").strip()
                
                if command.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                
                elif command.lower() == 'stats':
                    self.call_tool("get_lead_stats", {})
                
                elif command.lower() == 'demo':
                    self.run_demo()
                
                elif command.lower() == 'help':
                    self.show_help()
                
                elif command.lower().startswith('query '):
                    question = command[6:].strip()
                    if question:
                        self.call_tool("query_leads", {"question": question})
                    else:
                        print("❌ Please provide a question")
                
                elif command.lower().startswith('q '):
                    question = command[2:].strip()
                    if question:
                        self.call_tool("query_leads", {"question": question})
                    else:
                        print("❌ Please provide a question")
                
                elif command.lower() == '':
                    continue
                
                else:
                    # Try to interpret as a direct question
                    question_indicators = [
                        'how many', 'show me', 'give me', 'any leads', 'which leads',
                        'leads from', 'what', 'who', 'when', 'where', 'list',
                        'find', 'search', 'get', 'display', 'count'
                    ]
                    
                    is_question = any(indicator in command.lower() for indicator in question_indicators)
                    
                    if is_question:
                        print(f"🔍 Interpreting as question: '{command}'")
                        self.call_tool("query_leads", {"question": command})
                    else:
                        print("❌ Unknown command. Type 'help' for examples.")
                        print("💡 To ask a question, use: query <your question>")
                        print("   Or try: 'How many hot leads?' directly")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_help(self):
        """Show example questions"""
        print("\n📚 Example Questions:")
        print("\n📊 Counting:")
        print("  query How many leads do we have?")
        print("  query How many hot leads?")
        print("  query How many warm leads today?")
        
        print("\n🔍 Listing:")
        print("  query Show me all hot leads")
        print("  query Show me warm leads")
        print("  query Show me cold leads")
        
        print("\n🏢 Company Search:")
        print("  query Any leads from Microsoft?")
        print("  query Any leads from Google?")
        print("  query Leads from Facebook")
        
        print("\n🤖 AI Interest:")
        print("  query Which leads mention AI?")
        print("  query Show me leads with AI companies")
        
        print("\n📅 Time-based:")
        print("  query Leads from today")
        print("  query Leads from this week")

def main():
    """Main function"""
    cli = MCPTestCLI()
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        cli.run_demo()
    else:
        cli.interactive_mode()

if __name__ == "__main__":
    main()