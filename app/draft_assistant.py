import subprocess
import base64
import re

from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from app.auth import get_gmail_service

# ─── JINJA2 TEMPLATE SETUP ──────────────────────────────────────────────
TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)


def generate_templated_reply(template_name: str, context: dict) -> str:
    """
    Render a reply using a Jinja2 template.
    """
    template = env.get_template(template_name)
    return template.render(context)


# alias so your existing tests that do `from app.draft_assistant import generate_reply` still work
generate_reply = generate_templated_reply


# ─── DRAFTS / GMAIL UTILITIES ──────────────────────────────────────────
def get_drafts(max_results: int = 12) -> list:
    """
    List up to max_results drafts in the user's Gmail.
    """
    service = get_gmail_service()
    results = (
        service.users()
               .drafts()
               .list(userId="me", maxResults=max_results)
               .execute()
    )
    return results.get("drafts", [])


def get_draft_body(draft_id: str) -> str:
    """
    Fetch the plain-text body of a Gmail draft.
    """
    service = get_gmail_service()
    draft = (
        service.users()
               .drafts()
               .get(userId="me", id=draft_id, format="full")
               .execute()
    )
    payload = draft.get("message", {}).get("payload", {})

    # Top-level body
    body_data = payload.get("body", {}).get("data")
    if body_data:
        return base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")

    # Multipart fallback
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return ""


def is_safe_draft(text: str) -> bool:
    """
    Heuristic to skip drafts containing sensitive info.
    """
    # Skip if too short or mostly digits
    if len(text.strip()) < 20 or sum(c.isdigit() for c in text) > len(text) * 0.5:
        return False

    sensitive_patterns = [
        r"\b\d{10,11}\b",               # phone numbers
        r"\b[A-Z0-9]{8,}\b",            # token-like IDs
        r"(password|token|key|secret)", # keywords
        r"(agreement|welcome|SSE|@)",   # other private indicators
    ]
    for pattern in sensitive_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False

    return True


# ─── OLLAMA AI REPLY ─────────────────────────────────────────────────
def generate_ai_reply(text: str, model: str = "mistral") -> str:
    """
    Use Ollama to generate a professional reply to the given text.
    """
    prompt = f"Write a professional reply to this draft:\n\n{text}"

    try:
        process = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
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
