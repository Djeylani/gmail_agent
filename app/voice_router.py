import re
import os
import json
import time
from datetime import datetime
from pathlib import Path
from app.email_sender import send_email
from app.email_reader import get_sent_emails
from app.voice_to_email import transcribe_audio
from app.record_audio import record_audio
from app.contacts import resolve_contact, add_contact
from app.follow_up import run_follow_up_job
from app.drive_uploader import upload_to_drive

# Global settings
DEBUG_MODE = False
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
RECENT_CONTACTS = []

def interpret_command(transcript: str) -> str:
    transcript = transcript.lower()

    if "follow up" in transcript:
        return "follow_up"
    elif "unsubscribe" in transcript:
        return "unsubscribe"
    elif "summarize" in transcript:
        return "summarize"
    elif any(phrase in transcript for phrase in [
        "send an email", "compose an email", "write an email", "email saying", "email to"
    ]):
        return "compose_email"
    elif extract_email(transcript):
        return "compose_email"
    elif resolve_contact(transcript):
        return "compose_email"
    # Fallback: if it sounds like a message, treat as email
    elif any(word in transcript for word in ["will be", "running", "late", "meeting", "sorry", "can't", "won't"]):
        return "compose_email"
    else:
        return "unknown"

def extract_email(text: str) -> str | None:
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def log_interaction(transcript: str, intent: str, outcome: str, recipient: str = None):
    """Log interactions for training and analysis"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "transcript": transcript,
        "intent": intent,
        "outcome": outcome,
        "recipient": recipient
    }
    log_file = LOG_DIR / f"interactions_{datetime.now().strftime('%Y%m')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def get_last_recipient() -> str | None:
    if RECENT_CONTACTS:
        return RECENT_CONTACTS[-1]
    sent = get_sent_emails(max_results=1)
    if sent:
        headers = sent[0].get("payload", {}).get("headers", [])
        for h in headers:
            if h["name"].lower() == "to":
                return h["value"]
    return None

def get_recipient_from_voice() -> str | None:
    if DEBUG_MODE:
        response = input("🎤 [DEBUG] Enter recipient name or email: ").lower().strip()
    else:
        print("🎤 Say recipient name...")
        path = record_audio(filename="recipient.wav", duration=3)
        response = transcribe_audio(path, language="en").lower().strip()
    
    # Check for "last" command first
    if "last" in response or "same" in response:
        return get_last_recipient()

    # Try exact email match
    email = extract_email(response)
    if email:
        return email

    # Try contact resolution with lower threshold for better fuzzy matching
    resolved = resolve_contact(response, threshold=60)
    if resolved:
        return resolved

    # Single retry with different approach
    if not DEBUG_MODE:
        print("⚠️ Try again, speak clearly...")
        path = record_audio(filename="recipient2.wav", duration=2)
        response = transcribe_audio(path, language="en").lower().strip()
        resolved = resolve_contact(response, threshold=50)
        if resolved:
            return resolved
    
    return None

def compose_email_from_voice(transcript: str, audio_path="recordings/voice_note.wav", debug_mode=False):
    global DEBUG_MODE, RECENT_CONTACTS
    DEBUG_MODE = debug_mode
    
    recipient = get_recipient_from_voice()
    if not recipient:
        log_interaction(transcript, "compose_email", "failed_no_recipient")
        print("❌ No recipient found")
        return

    # Auto-add unknown emails to contacts
    if "@" in recipient and not resolve_contact(recipient):
        add_contact(recipient.split("@")[0], recipient)

    send_email(
        to=recipient,
        subject=f"Voice Note - {datetime.now().strftime('%H:%M')}",
        body=transcript.strip()
    )
    
    # Update cache
    if recipient not in RECENT_CONTACTS:
        RECENT_CONTACTS.append(recipient)
        RECENT_CONTACTS = RECENT_CONTACTS[-5:]  # Keep last 5
    
    log_interaction(transcript, "compose_email", "success", recipient)
    print(f"✅ Sent to {recipient.split('@')[0] if '@' in recipient else recipient}")