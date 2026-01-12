import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🚀 Running AI Lead Automation Pipeline\n")

os.system("python scripts/ingest_leads.py")
os.system("python scripts/score_leads.py")
os.system("python scripts/analytics.py")
os.system("python scripts/actions.py")

print("\n✅ Pipeline completed successfully")
