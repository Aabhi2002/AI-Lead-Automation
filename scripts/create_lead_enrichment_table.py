import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lead_enrichment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER UNIQUE,
        domain TEXT,
        website_exists INTEGER,
        has_pricing INTEGER,
        has_careers INTEGER,
        mentions_ai INTEGER,
        summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lead_id) REFERENCES leads(id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("lead_enrichment table created")
