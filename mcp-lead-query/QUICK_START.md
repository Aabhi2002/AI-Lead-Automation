# MCP Lead Query Agent - Quick Start

## 🚀 Start the CLI

```bash
python3 mcp-lead-query/mcp_cli_test.py
```

## 💬 How to Ask Questions

### ✅ Direct Questions (Recommended)
Just type your question naturally:
```
🎯 Command: How many hot leads?
🎯 Command: Give me all warm leads
🎯 Command: Any leads from Microsoft?
🎯 Command: Show me cold leads
```

### ✅ With Command Prefixes
```
🎯 Command: query How many hot leads?
🎯 Command: q Show me warm leads
```

### ✅ Special Commands
```
🎯 Command: stats        # Get lead statistics
🎯 Command: demo         # Run full demonstration
🎯 Command: help         # Show examples
🎯 Command: quit         # Exit
```

## 📊 Example Questions That Work

### Counting
- "How many leads do we have?"
- "How many hot leads?"
- "How many warm leads today?"

### Listing
- "Give me all warm leads"
- "Show me hot leads"
- "Show me cold leads"

### Company Search
- "Any leads from Microsoft?"
- "Leads from Facebook"
- "Any leads from Google?"

### AI Interest
- "Which leads mention AI?"
- "Show me leads with AI companies"

### Time-based
- "Leads from today"
- "Leads from this week"

## 🎯 Expected Results

Your database currently has:
- **15 total leads**
- **3 hot leads** (Microsoft, Shopify, TechCorp)
- **4 warm leads** (Facebook, Test Corp, TechStartup Inc, StartupIO)
- **8 cold leads** (Gmail users, low-quality domains)

## 🔧 Troubleshooting

**If a question doesn't work:**
1. Try adding "query" prefix: `query Your question here`
2. Check the help: `help`
3. See working examples: `demo`

**Common question patterns:**
- Start with: "How many...", "Show me...", "Give me...", "Any leads..."
- Include keywords: "hot", "warm", "cold", "leads", "from"

## ✨ Ready to Use!

Your MCP Lead Query Agent is working and ready to answer business questions about your leads!