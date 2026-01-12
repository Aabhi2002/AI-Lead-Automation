#!/usr/bin/env python3
"""
CLI interface for the MCP Lead Query Agent
Run this to interactively ask questions about your leads
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import LeadQueryAgent

def main():
    """Interactive CLI for lead queries"""
    agent = LeadQueryAgent()
    
    print("🤖 MCP Lead Query Agent - Interactive CLI")
    print("=" * 50)
    print("Ask me questions about your leads in plain English!")
    print()
    print("📝 Example questions:")
    print("  • 'How many warm leads today?'")
    print("  • 'Show me all hot leads'")
    print("  • 'Any leads from Microsoft?'")
    print("  • 'Which leads mention AI?'")
    print("  • 'How many leads this week?'")
    print()
    print("Type 'help' for more examples, 'quit' to exit.")
    print("=" * 50)
    print()
    
    while True:
        try:
            question = input("❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if question.lower() in ['help', 'h']:
                show_help()
                continue
            
            if not question:
                continue
            
            print(f"\n🔍 Processing: {question}")
            print("-" * 50)
            
            response = agent.answer_question(question)
            print(f"📊 {response}")
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def show_help():
    """Show help with example questions"""
    print("\n📚 Help - Example Questions:")
    print()
    print("📊 Counting Questions:")
    print("  • 'How many leads do we have?'")
    print("  • 'How many hot leads today?'")
    print("  • 'How many warm leads this week?'")
    print()
    print("🔍 Filtering Questions:")
    print("  • 'Show me all hot leads'")
    print("  • 'Show me warm leads from today'")
    print("  • 'Any leads from Microsoft?'")
    print("  • 'Which leads mention AI?'")
    print()
    print("📅 Time-based Questions:")
    print("  • 'Leads from today'")
    print("  • 'Leads from yesterday'")
    print("  • 'Leads from this week'")
    print()
    print("🏢 Company-based Questions:")
    print("  • 'Leads from Google'")
    print("  • 'Any leads from startups?'")
    print()
    print("🤖 AI-related Questions:")
    print("  • 'Which companies mention AI?'")
    print("  • 'Show leads with AI interest'")
    print()

if __name__ == "__main__":
    main()