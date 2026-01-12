import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an AI sales analyst.
Your job is to score inbound B2B leads.

Return ONLY valid JSON in this format:
{
  "score": float between 0 and 1,
  "category": "Cold" | "Warm" | "Hot",
  "action": "ignore" | "review" | "notify_sales",
  "reason": "short explanation"
}
"""

def score_lead(name, email, company, message, enrichment_summary):
    user_prompt = f"""
Lead details:
Name: {name}
Email: {email}
Company: {company}
Message: {message}

Company enrichment: {enrichment_summary}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)
 