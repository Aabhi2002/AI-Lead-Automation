import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_connection
from utils.validators import is_valid_email

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEADS_FILE = os.path.join(PROJECT_ROOT, "data", "leads.csv")

def ingest_leads():
    df = pd.read_csv(LEADS_FILE)

    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        email = row["email"]

        if not is_valid_email(email):
            skipped += 1
            continue

        try:
            cursor.execute("""
            INSERT INTO leads (name, email, company, message)
            VALUES (?, ?, ?, ?)
            """, (
                row["name"],
                email,
                row["company"],
                row["message"]
            ))
            inserted += 1
        except Exception:
            skipped += 1

    conn.commit()
    conn.close()

    print(f"Inserted: {inserted}, Skipped: {skipped}")

if __name__ == "__main__":
    ingest_leads()
