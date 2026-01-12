# MCP Lead Query Agent - Usage Guide

## 🎯 How to Test Your MCP Server

### Option 1: Interactive MCP CLI (Recommended)

Start the interactive MCP testing interface:

```bash
python3 mcp-lead-query/mcp_cli_test.py
```

**What you'll see:**
```
🤖 MCP Lead Query Server - Interactive Test Mode
============================================================

🔧 Available MCP Tools:
----------------------------------------
1. query_leads
   📝 Answer business questions about leads using natural language
   📋 Parameters:
      • question (required): Natural language question about leads

2. get_lead_stats
   📝 Get current lead statistics and metrics

💬 Commands:
  stats                    - Get lead statistics
  query <question>         - Ask about leads
  q <question>             - Short form query
  demo                     - Run demonstration
  help                     - Show example questions
  quit                     - Exit
============================================================

🎯 Command: _
```

### Option 2: Run Demo Mode

See all capabilities in action:

```bash
python3 mcp-lead-query/mcp_cli_test.py demo
```

This will automatically run through all MCP tools and show example queries.

### Option 3: Quick Start Script

```bash
python3 mcp-lead-query/start_mcp_cli.py
```

## 📝 Example MCP Commands

Once in the interactive CLI, try these commands:

### Get Statistics
```
🎯 Command: stats
```
**Output:**
```
Lead Statistics:
- Total Leads: 15
- Hot Leads: 3
- Warm Leads: 4
- Cold Leads: 8
```

### Ask Questions
```
🎯 Command: query How many hot leads do we have?
```
**Output:**
```
Found 3 matching leads.
```

```
🎯 Command: q Show me all hot leads
```
**Output:**
```
Found 3 matching leads:

Name | Email | Company | Category | Score | Time
--------------------------------------------------------------------------------
Lisa Wang | lisa@shopify.com | Shopify | Hot | 0.9 | 2026-01-05 12:01
Sarah Chen | sarah.chen@microsoft.com | Microsoft | Hot | 1.0 | 2026-01-05 12:00
Demo User | demo@techcorp.com | TechCorp | Hot | 0.8 | 2026-01-01 10:40
```

### Company-Specific Queries
```
🎯 Command: query Any leads from Microsoft?
```
**Output:**
```
Found 1 matching leads:

Name | Email | Company | Category | Score | Time
--------------------------------------------------------------------------------
Sarah Chen | sarah.chen@microsoft.com | Microsoft | Hot | 1.0 | 2026-01-05 12:00
```

### AI Interest Detection
```
🎯 Command: query Which leads mention AI?
```
**Output:**
```
Found 5 matching leads:

Name | Email | Company | Category | Score | Time
--------------------------------------------------------------------------------
Lisa Wang | lisa@shopify.com | Shopify | Hot | 0.9 | 2026-01-05 12:01
Sarah Chen | sarah.chen@microsoft.com | Microsoft | Hot | 1.0 | 2026-01-05 12:00
Demo User | demo@techcorp.com | TechCorp | Hot | 0.8 | 2026-01-01 10:40
Test User | test@example.com | Test Corp | Warm | 0.7 | 2026-01-01 10:35
Anita | anita@startup.io | StartupIO | Warm | 0.8 | 2025-12-30 11:38
```

## 🔧 MCP Protocol Testing

### What the CLI Tests

1. **MCP Tools Discovery**: Lists available tools and their schemas
2. **Tool Execution**: Calls tools with proper JSON-RPC format
3. **Response Handling**: Processes MCP server responses
4. **Error Handling**: Shows how errors are handled in MCP protocol

### MCP Request/Response Format

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "query_leads",
    "arguments": {
      "question": "How many hot leads?"
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "content": [
    {
      "type": "text",
      "text": "Found 3 matching leads."
    }
  ]
}
```

## 🧪 Testing Different Scenarios

### 1. Counting Queries
- `stats` - Overall statistics
- `query How many leads do we have?`
- `query How many hot leads?`
- `query How many warm leads today?`

### 2. Listing Queries
- `query Show me all hot leads`
- `query Show me warm leads`
- `query Show me cold leads`

### 3. Company Filtering
- `query Any leads from Microsoft?`
- `query Any leads from Google?`
- `query Leads from Facebook`

### 4. AI Interest Detection
- `query Which leads mention AI?`
- `query Show me leads with AI companies`

### 5. Time-based Queries
- `query Leads from today`
- `query Leads from this week`
- `query Leads from yesterday`

### 6. Edge Cases
- Empty questions
- Unrecognized patterns
- Invalid company names

## 🎯 Expected Results

Based on your current database:

- **Total Leads**: 15
- **Hot Leads**: 3 (Microsoft, Shopify, TechCorp)
- **Warm Leads**: 4 (Facebook, Test Corp, TechStartup Inc, StartupIO)
- **Cold Leads**: 8 (Gmail users, domains without websites)
- **AI-Interested**: 5 leads mention AI in their enrichment data

## 🚀 Next Steps

1. **Test Basic Functionality**: Run `python3 mcp-lead-query/mcp_cli_test.py demo`
2. **Try Interactive Mode**: Run `python3 mcp-lead-query/mcp_cli_test.py`
3. **Ask Your Own Questions**: Use the `query` command with your business questions
4. **Integrate with MCP Client**: Use the MCP server in your preferred MCP client application

Your MCP Lead Query Agent is ready for production use!