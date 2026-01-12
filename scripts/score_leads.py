import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_connection
from utils.ai import score_lead

def score_all_leads():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        l.id,
        l.name,
        l.email,
        l.company,
        l.message,
        e.summary
    FROM leads l
    LEFT JOIN lead_enrichment e ON l.id = e.lead_id
    WHERE l.id NOT IN (SELECT lead_id FROM lead_scores)
    """)

    leads = cursor.fetchall()

    for lead in leads:
        lead_id, name, email, company, message, enrichment_summary = lead

        ai_result = score_lead(
            name,
            email,
            company,
            message,
            enrichment_summary or "No enrichment data available"
        )

        cursor.execute("""
        INSERT INTO lead_scores (lead_id, score, category, action, reason)
        VALUES (?, ?, ?, ?, ?)
        """, (
            lead_id,
            ai_result["score"],
            ai_result["category"],
            ai_result["action"],
            ai_result["reason"]
        ))

        print(f"Scored lead {email}: {ai_result['category']}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    score_all_leads()
