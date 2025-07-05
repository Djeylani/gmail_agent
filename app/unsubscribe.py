import webbrowser
import re
import base64
import smtplib
from email.message import EmailMessage
from app.auth import get_gmail_service

# Unsubscribe from mailing lists using Gmail API

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
    ...
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "me"
    msg['To'] = to_address
    msg.set_content("Please unsubscribe me from this mailing list.")

    raw_bytes = msg.as_bytes()
    encoded_msg = base64.urlsafe_b64encode(raw_bytes).decode()

    service = get_gmail_service()
    try:
        service.users().messages().send(userId='me', body={'raw': encoded_msg}).execute()
        print("✅ Unsubscribe email sent.")
    except Exception as e:
        print(f"❌ Failed to send unsubscribe email: {e}")


# Archive and label the message after unsubscribing
def archive_and_label_message(message_id, label_name="Unsubscribed"):
    service = get_gmail_service()

    # Ensure label exists or create it
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    label_id = next((l['id'] for l in labels if l['name'] == label_name), None)

    if not label_id:
        label = service.users().labels().create(userId='me', body={
            'name': label_name,
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show'
        }).execute()
        label_id = label['id']

    # Modify the message: remove INBOX, add label
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={
            'removeLabelIds': ['INBOX'],
            'addLabelIds': [label_id]
        }
    ).execute()
    print(f"📦 Archived and labeled message {message_id} as '{label_name}'")
