import sys
import os
# Fix import path to access utils and scripts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3

# Import existing business logic (DO NOT MODIFY)
from utils.db import get_connection
from utils.validators import is_valid_email
from utils.enrichment import extract_domain, check_website, extract_signals, is_public_email
from utils.ai import score_lead

app = FastAPI(title="Lead Automation API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class LeadSubmission(BaseModel):
    name: str
    email: str
    company: str
    message: str

# Response models
class LeadResponse(BaseModel):
    score: float
    category: str
    action: str
    reason: str
    enrichment_summary: str

class MetricsResponse(BaseModel):
    total_leads: int
    hot_leads: int
    warm_leads: int
    cold_leads: int
    avg_score: float

@app.get("/")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Lead Automation API is running"}

@app.post("/submit-lead", response_model=LeadResponse)
def submit_lead(lead: LeadSubmission):
    """
    Submit a new lead and get AI scoring result.
    Wraps existing ingest -> enrich -> score pipeline.
    """
    # Validate email using existing logic
    if not is_valid_email(lead.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Step 1: Insert lead (reusing ingest_leads.py logic)
        cursor.execute("""
        INSERT INTO leads (name, email, company, message)
        VALUES (?, ?, ?, ?)
        """, (lead.name, lead.email, lead.company, lead.message))
        
        lead_id = cursor.lastrowid
        
        # Step 2: Enrich lead (reusing enrich_leads.py logic)
        domain = extract_domain(lead.email)
        
        if is_public_email(domain):
            # Public email handling
            website_exists = False
            signals = {"has_pricing": 0, "has_careers": 0, "mentions_ai": 0}
            enrichment_summary = "Public email domain detected (low business confidence)"
        else:
            # Business domain enrichment
            website_exists, page_text = check_website(domain)
            signals = extract_signals(page_text) if website_exists else {
                "has_pricing": 0, "has_careers": 0, "mentions_ai": 0
            }
            enrichment_summary = (
                f"Website exists: {website_exists}, "
                f"Pricing: {signals['has_pricing']}, "
                f"Careers: {signals['has_careers']}, "
                f"Mentions AI: {signals['mentions_ai']}"
            )
        
        # Store enrichment
        cursor.execute("""
        INSERT INTO lead_enrichment
        (lead_id, domain, website_exists, has_pricing, has_careers, mentions_ai, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lead_id, domain, int(website_exists),
            signals["has_pricing"], signals["has_careers"], signals["mentions_ai"],
            enrichment_summary
        ))
        
        # Step 3: Score lead (reusing score_leads.py logic)
        ai_result = score_lead(
            lead.name, lead.email, lead.company, lead.message, enrichment_summary
        )
        
        # Store score
        cursor.execute("""
        INSERT INTO lead_scores (lead_id, score, category, action, reason)
        VALUES (?, ?, ?, ?, ?)
        """, (
            lead_id, ai_result["score"], ai_result["category"],
            ai_result["action"], ai_result["reason"]
        ))
        
        conn.commit()
        
        # Return combined result
        return LeadResponse(
            score=ai_result["score"],
            category=ai_result["category"],
            action=ai_result["action"],
            reason=ai_result["reason"],
            enrichment_summary=enrichment_summary
        )
        
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    finally:
        conn.close()

@app.get("/metrics", response_model=MetricsResponse)
def get_metrics():
    """
    Get current lead metrics.
    Always calculates real-time metrics for the internal ops UI.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Always calculate real-time metrics for internal ops UI
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
        
        return MetricsResponse(
            total_leads=total_leads,
            hot_leads=category_counts.get("Hot", 0),
            warm_leads=category_counts.get("Warm", 0),
            cold_leads=category_counts.get("Cold", 0),
            avg_score=round(avg_score, 2)
        )
        
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)