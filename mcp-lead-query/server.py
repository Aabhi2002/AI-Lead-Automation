#!/usr/bin/env python3
"""
MCP-powered Data Query Agent for Lead Management System
Converts natural language business questions into safe SQL queries
"""

import json
import sqlite3
import re
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
import sys
import os

# Add parent directory to path to access utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db import get_connection

class LeadQueryAgent:
    """MCP-powered agent that answers business questions about leads"""
    
    def __init__(self):
        self.db_path = "../db/database.db"
        
    def execute_query(self, sql: str, params: tuple = ()) -> List[Dict]:
        """Execute a read-only SQL query safely"""
        # Ensure query is read-only
        sql_upper = sql.upper().strip()
        if not sql_upper.startswith('SELECT'):
            raise ValueError("Only SELECT queries are allowed")
        
        # Block dangerous keywords (but not when they're part of column names)
        dangerous_patterns = [
            r'\bINSERT\b', r'\bUPDATE\b', r'\bDELETE\b', 
            r'\bDROP\b', r'\bALTER\b', r'\bCREATE\s+TABLE\b',
            r'\bCREATE\s+INDEX\b', r'\bCREATE\s+VIEW\b'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, sql_upper):
                raise ValueError(f"Query contains forbidden pattern: {pattern}")
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Fetch results and convert to list of dicts
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            conn.close()
            return results
            
        except sqlite3.Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def translate_question(self, question: str) -> str:
        """Convert natural language question to SQL query"""
        question_lower = question.lower().strip()
        
        # Base query components
        base_select = """
        SELECT 
            l.name,
            l.email, 
            l.company,
            ls.category,
            ls.score,
            l.created_at
        FROM leads l
        LEFT JOIN lead_scores ls ON l.id = ls.lead_id
        """
        
        conditions = []
        
        # Date filters
        if 'today' in question_lower:
            conditions.append("DATE(l.created_at) = DATE('now')")
        elif 'yesterday' in question_lower:
            conditions.append("DATE(l.created_at) = DATE('now', '-1 day')")
        elif 'this week' in question_lower or 'last 7 days' in question_lower:
            conditions.append("DATE(l.created_at) >= DATE('now', '-7 days')")
        
        # Category filters (case-sensitive)
        if 'hot lead' in question_lower:
            conditions.append("ls.category = 'Hot'")
        elif 'warm lead' in question_lower:
            conditions.append("ls.category = 'Warm'")
        elif 'cold lead' in question_lower:
            conditions.append("ls.category = 'Cold'")
        
        # Company filters
        company_match = re.search(r'from\s+(\w+)', question_lower)
        if company_match:
            company = company_match.group(1)
            conditions.append(f"l.company LIKE '%{company}%'")
        
        # AI-related filters
        if 'ai' in question_lower and ('mention' in question_lower or 'companies' in question_lower):
            base_select = """
            SELECT 
                l.name,
                l.email, 
                l.company,
                ls.category,
                ls.score,
                l.created_at
            FROM leads l
            LEFT JOIN lead_scores ls ON l.id = ls.lead_id
            LEFT JOIN lead_enrichment le ON l.id = le.lead_id
            """
            conditions.append("le.mentions_ai = 1")
        
        # Count queries
        if question_lower.startswith('how many') or 'count' in question_lower:
            base_select = "SELECT COUNT(*) as count FROM leads l LEFT JOIN lead_scores ls ON l.id = ls.lead_id"
        
        # Build final query
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)
        
        order_clause = ""
        if 'COUNT(*)' not in base_select:
            order_clause = " ORDER BY l.created_at DESC LIMIT 50"
        
        sql = base_select + where_clause + order_clause
        return sql
    
    def format_response(self, results: List[Dict], question: str) -> str:
        """Format query results into structured response"""
        if not results:
            return "No matching leads found."
        
        # Handle count queries
        if len(results) == 1 and 'count' in results[0]:
            count = results[0]['count']
            return f"Found {count} matching leads."
        
        # Regular lead queries
        count = len(results)
        response_lines = [f"Found {count} matching leads:\n"]
        
        # Header
        response_lines.append("Name | Email | Company | Category | Score | Time")
        response_lines.append("-" * 80)
        
        # Data rows
        for lead in results:
            name = lead.get('name', 'N/A')
            email = lead.get('email', 'N/A')
            company = lead.get('company', 'N/A')
            category = lead.get('category', 'N/A')
            score = lead.get('score', 'N/A')
            if score != 'N/A':
                score = f"{score:.1f}"
            
            # Format timestamp
            created_at = lead.get('created_at', '')
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    time_str = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    time_str = created_at[:16]  # Fallback
            else:
                time_str = 'N/A'
            
            response_lines.append(f"{name} | {email} | {company} | {category} | {score} | {time_str}")
        
        return "\n".join(response_lines)
    
    def answer_question(self, question: str) -> str:
        """Main method to answer business questions about leads"""
        try:
            # Validate input
            if not question or not question.strip():
                return "Please ask a specific question about leads."
            
            # Translate to SQL
            sql = self.translate_question(question)
            
            # Execute query
            results = self.execute_query(sql)
            
            # Format response
            response = self.format_response(results, question)
            
            return response
            
        except ValueError as e:
            return f"Query error: {str(e)}"
        except Exception as e:
            return f"I don't have enough data to answer this. Error: {str(e)}"

def main():
    """CLI interface for testing the query agent"""
    agent = LeadQueryAgent()
    
    print("🤖 MCP Lead Query Agent")
    print("Ask me questions about your leads!")
    print("Examples:")
    print("- 'How many warm leads today?'")
    print("- 'Show me all hot leads'")
    print("- 'Any leads from Microsoft?'")
    print("- 'Which leads mention AI?'")
    print("\nType 'quit' to exit.\n")
    
    while True:
        try:
            question = input("❓ Question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not question:
                continue
            
            print(f"\n🔍 Processing: {question}")
            response = agent.answer_question(question)
            print(f"\n📊 Answer:\n{response}\n")
            print("-" * 80)
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()