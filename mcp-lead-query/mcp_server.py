#!/usr/bin/env python3
"""
MCP Server for Lead Query Agent
Implements Model Context Protocol for natural language lead queries
"""

import json
import sys
from typing import Any, Dict, List
from server import LeadQueryAgent

class MCPLeadQueryServer:
    """MCP Server that handles lead query requests"""
    
    def __init__(self):
        self.agent = LeadQueryAgent()
        self.tools = [
            {
                "name": "query_leads",
                "description": "Answer business questions about leads using natural language",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Natural language question about leads (e.g., 'How many warm leads today?', 'Show me hot leads from Microsoft')"
                        }
                    },
                    "required": ["question"]
                }
            },
            {
                "name": "get_lead_stats",
                "description": "Get current lead statistics and metrics",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "tools/list":
            return {
                "tools": self.tools
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "query_leads":
                question = arguments.get("question", "")
                result = self.agent.answer_question(question)
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
            
            elif tool_name == "get_lead_stats":
                # Get overall statistics
                stats_query = "SELECT COUNT(*) as total FROM leads"
                total_results = self.agent.execute_query(stats_query)
                
                category_query = """
                SELECT ls.category, COUNT(*) as count 
                FROM lead_scores ls 
                GROUP BY ls.category
                """
                category_results = self.agent.execute_query(category_query)
                
                # Format stats
                total_leads = total_results[0]['total'] if total_results else 0
                stats = {"total_leads": total_leads}
                
                for row in category_results:
                    category = row['category'].lower() + "_leads"
                    stats[category] = row['count']
                
                stats_text = f"""Lead Statistics:
- Total Leads: {stats.get('total_leads', 0)}
- Hot Leads: {stats.get('hot_leads', 0)}
- Warm Leads: {stats.get('warm_leads', 0)}
- Cold Leads: {stats.get('cold_leads', 0)}"""
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": stats_text
                        }
                    ]
                }
            
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
        
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }

def main():
    """Run the MCP server"""
    server = MCPLeadQueryServer()
    
    # Print startup info to stderr (not stdout which is used for JSON-RPC)
    print("🚀 MCP Lead Query Server started", file=sys.stderr)
    print("Available tools:", file=sys.stderr)
    for tool in server.tools:
        print(f"  - {tool['name']}: {tool['description']}", file=sys.stderr)
    print("Ready for requests...", file=sys.stderr)
    sys.stderr.flush()
    
    # Read JSON-RPC requests from stdin
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            try:
                request = json.loads(line)
                response = server.handle_request(request)
                
                # Add request ID if present
                if "id" in request:
                    response["id"] = request["id"]
                
                # Add JSON-RPC version
                response["jsonrpc"] = "2.0"
                
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                if "id" in locals() and isinstance(locals().get("request"), dict):
                    error_response["id"] = request.get("id")
                print(json.dumps(error_response), flush=True)
                
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                if "request" in locals() and isinstance(request, dict):
                    error_response["id"] = request.get("id")
                print(json.dumps(error_response), flush=True)
                
    except KeyboardInterrupt:
        print("Server shutting down...", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()