import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_connection
from datetime import date

def generate_daily_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM leads")
    total_leads = cursor.fetchone()[0]

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM lead_scores
        GROUP BY category
    """)
    category_counts = dict(cursor.fetchall())

    cursor.execute("SELECT AVG(score) FROM lead_scores")
    avg_score = cursor.fetchone()[0] or 0

    metrics = {
        "date": str(date.today()),
        "total_leads": total_leads,
        "hot_leads": category_counts.get("Hot", 0),
        "warm_leads": category_counts.get("Warm", 0),
        "cold_leads": category_counts.get("Cold", 0),
        "avg_score": round(avg_score, 2)
    }

    cursor.execute("""
        INSERT INTO daily_metrics
        (date, total_leads, hot_leads, warm_leads, cold_leads, avg_score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        metrics["date"],
        metrics["total_leads"],
        metrics["hot_leads"],
        metrics["warm_leads"],
        metrics["cold_leads"],
        metrics["avg_score"]
    ))

    conn.commit()
    conn.close()

    return metrics
 
if __name__ == "__main__":
    metrics = generate_daily_metrics()
    print("Daily Metrics Generated:")
    for k, v in metrics.items():
        print(f"{k}: {v}")
