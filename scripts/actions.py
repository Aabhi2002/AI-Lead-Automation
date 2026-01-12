import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_connection

def notify_sales(email, reason):
    # In real life: Slack / Email / CRM
    print(f"[SALES ALERT] {email} | Reason: {reason}")

def add_to_review_queue(email, reason):
    print(f"[REVIEW QUEUE] {email} | Reason: {reason}")

def ignore_lead(email):
    print(f"[IGNORED] {email}")

def run_actions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT l.email, s.action, s.reason
        FROM lead_scores s
        JOIN leads l ON s.lead_id = l.id
    """)

    rows = cursor.fetchall()

    for email, action, reason in rows:
        if action == "notify_sales":
            notify_sales(email, reason)
        elif action == "review":
            add_to_review_queue(email, reason)
        elif action == "ignore":
            ignore_lead(email)

    conn.close()

if __name__ == "__main__":
    run_actions()
