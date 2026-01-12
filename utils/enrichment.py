import requests

PUBLIC_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "icloud.com"
}

def extract_domain(email):
    return email.split("@")[-1].lower()

def is_public_email(domain):
    return domain in PUBLIC_EMAIL_DOMAINS

def check_website(domain):
    try:
        url = f"https://{domain}"
        response = requests.get(url, timeout=5)
        return response.status_code == 200, response.text.lower()
    except:
        return False, ""

def extract_signals(page_text):
    return {
        "has_pricing": int("pricing" in page_text),
        "has_careers": int("careers" in page_text or "jobs" in page_text),
        "mentions_ai": int("ai" in page_text or "artificial intelligence" in page_text)
    }
