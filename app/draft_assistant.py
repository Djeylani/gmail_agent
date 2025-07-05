import subprocess
import base64
import re
from app.auth import get_gmail_service

def get_drafts(max_results=12):
    service = get_gmail_service()
    results = service.users().drafts().list(userId='me', maxResults=max_results).execute()
    return results.get('drafts', [])

def get_draft_body(draft_id):
    service = get_gmail_service()
    draft = service.users().drafts().get(userId='me', id=draft_id, format='full').execute()
    message = draft.get('message', {})
    payload = message.get('payload', {})

    # Try top-level body
    body_data = payload.get('body', {}).get('data')
    if body_data:
        return base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')

    # Try multipart
    parts = payload.get('parts', [])
    for part in parts:
        if part.get('mimeType') == 'text/plain':
            data = part.get('body', {}).get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

    return ""

def is_safe_draft(text):
    sensitive_patterns = [
        r"\b\d{10,11}\b",                     # Phone numbers
        r"\b[A-Z0-9]{8,}\b",                  # Agreement or token-like IDs
        r"(password|token|key|secret)",       # Sensitive keywords
        r"(agreement|welcome|SSE|@)",         # Other private indicators
    ]
    # Skip if it's too short or mostly numeric
    if len(text.strip()) < 20 or sum(c.isdigit() for c in text) > len(text) * 0.5:
        return False

    for pattern in sensitive_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False
    return True

def generate_reply(text, model="mistral"):
    try:
        prompt = f"Write a professional reply to this draft:\n\n{text}"
        process = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=prompt, timeout=60)
        return stdout.strip()
    except subprocess.TimeoutExpired:
        process.kill()
        print("⚠️ Ollama timed out. Try a shorter input or increase timeout.")
        return "[Timeout: No reply generated]"
    except Exception as e:
        print(f"❌ Ollama failed: {e}")
        return "[Error: No reply generated]"
