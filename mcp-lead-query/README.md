# MCP Lead Query Agent

An MCP-powered Data Query Agent that converts plain English business questions into safe, read-only SQL queries for your lead management system.

## 🎯 What It Does

The agent answers business questions about your leads using **ONLY** real database data. It converts natural language questions into safe SQL queries and returns structured results.

## 📊 Database Schema

The agent works with your existing lead management database:

- **leads**: id, name, email, company, message, created_at
- **lead_scores**: lead_id, score, category (Hot/Warm/Cold), action, reason
- **lead_enrichment**: lead_id, domain, website_exists, has_pricing, mentions_ai
- **daily_metrics**: date, total_leads, hot_leads, warm_leads, cold_leads

## 🚀 Quick Start

### MCP CLI Testing (Recommended)
```bash
# Interactive MCP testing
python3 mcp-lead-query/mcp_cli_test.py

# Run MCP demo
python3 mcp-lead-query/mcp_cli_test.py demo

# Quick start script
python3 mcp-lead-query/start_mcp_cli.py
```

### Direct Agent Testing
```bash
# Interactive CLI (direct agent)
python3 mcp-lead-query/cli.py

# Run comprehensive tests
python3 mcp-lead-query/test_agent.py

# Test MCP server directly
python3 mcp-lead-query/test_mcp.py
```

### Use as Module
```python
from server import LeadQueryAgent

agent = LeadQueryAgent()
result = agent.answer_question("How many hot leads today?")
print(result)
```

## 💬 Example Questions

### 📊 Counting Questions
- "How many leads do we have?"
- "How many hot leads today?"
- "How many warm leads this week?"

### 🔍 Filtering Questions
- "Show me all hot leads"
- "Show me warm leads from today"
- "Any leads from Microsoft?"
- "Which leads mention AI?"

### 📅 Time-based Questions
- "Leads from today"
- "Leads from yesterday"
- "Leads from this week"

### 🏢 Company-based Questions
- "Leads from Google"
- "Any leads from startups?"

## 📋 Sample Output

```
❓ Question: Show me all hot leads

📊 Answer:
Found 3 matching leads:

Name | Email | Company | Category | Score | Time
--------------------------------------------------------------------------------
Lisa Wang | lisa@shopify.com | Shopify | Hot | 0.9 | 2026-01-05 12:01
Sarah Chen | sarah.chen@microsoft.com | Microsoft | Hot | 1.0 | 2026-01-05 12:00
Demo User | demo@techcorp.com | TechCorp | Hot | 0.8 | 2026-01-01 10:40
```

## 🔒 Safety Features

### Strict Security Rules
1. **READ-ONLY**: Only SELECT queries allowed
2. **NO HALLUCINATION**: Only returns real database data
3. **SAFE SQL**: Blocks dangerous keywords and patterns
4. **INPUT VALIDATION**: Sanitizes all user input

### Query Safety Checks
- Blocks INSERT, UPDATE, DELETE operations
- Prevents DROP, ALTER, CREATE TABLE statements
- Uses parameterized queries when possible
- Validates SQL structure before execution

## 🧪 Test Results

The comprehensive test suite shows the agent correctly handles:

✅ **15 total leads** in database  
✅ **3 hot leads** (Microsoft, Shopify, TechCorp)  
✅ **4 warm leads** (Facebook, Test Corp, TechStartup Inc, StartupIO)  
✅ **8 cold leads** (Gmail users, domains without websites)  
✅ **Company filtering** (Microsoft, Facebook, etc.)  
✅ **AI interest detection** (5 leads mention AI)  
✅ **Time-based queries** (today, yesterday, this week)  
✅ **Error handling** (empty questions, unrecognized patterns)  

## 🏗️ Architecture

```
mcp-lead-query/
├── server.py          # Main LeadQueryAgent class
├── mcp_server.py      # MCP protocol implementation
├── cli.py             # Interactive command-line interface
├── test_agent.py      # Comprehensive test suite
└── README.md          # This documentation
```

### Core Components

1. **LeadQueryAgent**: Main class that handles question translation and query execution
2. **Query Translator**: Converts natural language to SQL using pattern matching
3. **Safety Layer**: Validates queries to ensure read-only access
4. **Response Formatter**: Structures results in human-readable format

## 🔧 Technical Details

### Query Translation Logic
- **Date filters**: "today" → `DATE(created_at) = DATE('now')`
- **Category filters**: "hot leads" → `category = 'Hot'`
- **Company filters**: "from Microsoft" → `company LIKE '%Microsoft%'`
- **AI filters**: "mention AI" → `mentions_ai = 1`

### Default Behavior
- Sort by `created_at DESC` (most recent first)
- Limit results to 50 unless specified otherwise
- Join `leads` + `lead_scores` for category filtering
- Case-sensitive category matching: 'Hot', 'Warm', 'Cold'

## 🎯 Use Cases

### Sales Team
- "How many hot leads this week?"
- "Show me leads from enterprise companies"
- "Which leads need follow-up?"

### Marketing Team
- "How many leads from our AI campaign?"
- "Show me leads from tech companies"
- "What's our conversion rate?"

### Management
- "Overall lead statistics"
- "Top performing lead sources"
- "Weekly lead trends"

## 🚦 Status

✅ **Fully Functional**: All core features working  
✅ **Tested**: Comprehensive test suite passes  
✅ **Safe**: Read-only queries with security validation  
✅ **Fast**: Direct SQL queries, no external dependencies  
✅ **Accurate**: Only returns real database data  

## 🔮 Future Enhancements

- [ ] More sophisticated NLP for complex questions
- [ ] Support for date ranges ("leads from last month")
- [ ] Aggregation queries ("average score by company")
- [ ] Export results to CSV/JSON
- [ ] Integration with MCP client applications

---

**Ready to use!** The MCP Lead Query Agent is production-ready and can answer business questions about your leads immediately.