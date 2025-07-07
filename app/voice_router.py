from app.email_sender import send_email
from app.email_reader import get_sent_emails
import re

def get_last_recipient():
    sent = get_sent_emails(max_results=1)
    if sent:
        headers = sent[0].get("payload", {}).get("headers", [])
        for h in headers:
            if h["name"].lower() == "to":
                return h["value"]
    return None

def dispatch_command(intent: str, transcript: str):
    if intent == "compose_email":
        recipient = extract_email(transcript)

        if not recipient:
            print("🤖 Who should I send this to?")
            recipient_input = input("🎤 You: ").strip().lower()

            if "last" in recipient_input:
                recipient = get_last_recipient()
                if not recipient:
                    print("⚠️ Couldn't find the last recipient.")
                    return
                print(f"📨 Sending to your last contact: {recipient}")
            else:
                recipient = recipient_input

        email = {
            "to": recipient,
            "subject": "Voice Composed Email",
            "body": transcript
        }
        send_email(**email)
        print(f"✅ Email sent to {recipient}")

        
def extract_email(text: str) -> str | None:
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None
