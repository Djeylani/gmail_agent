import webbrowser
import re
import smtplib
from email.message import EmailMessage
from app.auth import get_gmail_service

def extract_unsubscribe_links(message_id):
    service = get_gmail_service()
    msg = service.users().messages().get(userId='me', id=message_id, format='metadata', metadataHeaders=['List-Unsubscribe']).execute()
    
    headers = msg.get('payload', {}).get('headers', [])
    unsubscribe_header = next((h['value'] for h in headers if h['name'].lower() == 'list-unsubscribe'), None)

    if not unsubscribe_header:
        return []

    links = [link.strip('<> ') for link in unsubscribe_header.split(',')]
    return links

def trigger_unsubscribe(link):
    if link.startswith("http"):
        print(f"🌐 Opening unsubscribe URL: {link}")
        webbrowser.open(link)
    elif link.startswith("mailto:"):
        print(f"📧 Sending unsubscribe email to: {link}")
        send_unsubscribe_email(link)

def send_unsubscribe_email(mailto_link):
    match = re.match(r'mailto:(.+?)(\?.*)?', mailto_link)
    if not match:
        print("❌ Invalid mailto link.")
        return

    to_address = match.group(1)
    subject = "Unsubscribe"
    if match.group(2):
        query = match.group(2)
        subject_match = re.search(r'subject=([^&]+)', query)
        if subject_match:
            subject = subject_match.group(1)

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "me"
    msg['To'] = to_address
    msg.set_content("Please unsubscribe me from this mailing list.")

    # Send via Gmail API
    service = get_gmail_service()
    encoded_msg = {'raw': msg.as_bytes().decode('utf-8')}
    try:
        service.users().messages().send(userId='me', body=encoded_msg).execute()
        print("✅ Unsubscribe email sent.")
    except Exception as e:
        print(f"❌ Failed to send unsubscribe email: {e}")
