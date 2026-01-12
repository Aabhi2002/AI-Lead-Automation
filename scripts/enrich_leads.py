import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_connection
from utils.enrichment import extract_domain, check_website, extract_signals, is_public_email

def enrich_leads():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT l.id, l.email
        FROM leads l
        WHERE l.id NOT IN (SELECT lead_id FROM lead_enrichment)
    """)

    leads = cursor.fetchall()

    for lead_id, email in leads:
        domain = extract_domain(email)
        
        # 🚨 Public email handling
        if is_public_email(domain):
            website_exists = False
            signals = {
                "has_pricing": 0,
                "has_careers": 0,
                "mentions_ai": 0
            }
            summary = "Public email domain detected (low business confidence)"
        else:
            website_exists, page_text = check_website(domain)
            signals = extract_signals(page_text) if website_exists else {
                "has_pricing": 0,
                "has_careers": 0,
                "mentions_ai": 0
            }
            summary = (
                f"Website exists: {website_exists}, "
                f"Pricing: {signals['has_pricing']}, "
                f"Careers: {signals['has_careers']}, "
                f"Mentions AI: {signals['mentions_ai']}"
            )

        cursor.execute("""
            INSERT INTO lead_enrichment
            (lead_id, domain, website_exists, has_pricing, has_careers, mentions_ai, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lead_id,
            domain,
            int(website_exists),
            signals["has_pricing"],
            signals["has_careers"],
            signals["mentions_ai"],
            summary
        ))

        print(f"Enriched {email} → {summary}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    enrich_leads()
