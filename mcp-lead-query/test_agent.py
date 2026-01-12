#!/usr/bin/env python3
"""
Comprehensive test suite for the MCP Lead Query Agent
Demonstrates all capabilities with various question types
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import LeadQueryAgent

def run_tests():
    """Run comprehensive tests of the query agent"""
    agent = LeadQueryAgent()
    
    print("🧪 MCP Lead Query Agent - Comprehensive Test Suite")
    print("=" * 60)
    print()
    
    test_questions = [
        # Counting questions
        ("How many leads do we have?", "📊 Total Lead Count"),
        ("How many hot leads?", "🔥 Hot Lead Count"),
        ("How many warm leads?", "🌡️ Warm Lead Count"),
        ("How many cold leads?", "❄️ Cold Lead Count"),
        ("How many hot leads today?", "📅 Hot Leads Today"),
        
        # Listing questions
        ("Show me all hot leads", "🔥 All Hot Leads"),
        ("Show me all warm leads", "🌡️ All Warm Leads"),
        ("Show me all cold leads", "❄️ All Cold Leads"),
        
        # Company-specific questions
        ("Any leads from Microsoft?", "🏢 Microsoft Leads"),
        ("Any leads from Google?", "🏢 Google Leads"),
        ("Any leads from Facebook?", "🏢 Facebook Leads"),
        
        # Time-based questions
        ("Leads from today", "📅 Today's Leads"),
        ("Leads from yesterday", "📅 Yesterday's Leads"),
        ("Leads from this week", "📅 This Week's Leads"),
        
        # AI-related questions
        ("Which leads mention AI?", "🤖 AI-Interested Leads"),
        ("Show me leads with AI companies", "🤖 AI Companies"),
        
        # Edge cases
        ("", "❌ Empty Question"),
        ("xyz random question", "❓ Unrecognized Question"),
    ]
    
    for i, (question, description) in enumerate(test_questions, 1):
        print(f"Test {i:2d}: {description}")
        print(f"Question: '{question}'")
        print("-" * 50)
        
        try:
            if question:
                response = agent.answer_question(question)
                print(f"Response: {response}")
            else:
                print("Response: Skipped empty question")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print()
    
    print("=" * 60)
    print("✅ Test suite completed!")

def demo_interactive():
    """Demo the interactive capabilities"""
    agent = LeadQueryAgent()
    
    print("\n🎯 Interactive Demo")
    print("=" * 30)
    
    demo_questions = [
        "How many leads do we have?",
        "Show me all hot leads",
        "Any leads from Microsoft?",
        "How many warm leads today?"
    ]
    
    for question in demo_questions:
        print(f"\n❓ Question: {question}")
        response = agent.answer_question(question)
        print(f"📊 Answer: {response}")
        print("-" * 30)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_interactive()
    else:
        run_tests()