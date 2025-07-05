from app.auth import get_gmail_service

def get_unread_emails(max_results=10):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        q='is:unread',
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])
    email_data = []

    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_detail.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        from_ = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
        snippet = msg_detail.get('snippet', '')
        email_data.append({
            'id': msg['id'],
            'from': from_,
            'subject': subject,
            'snippet': snippet
        })

    return email_data

def get_thread_text(message_id):
    service = get_gmail_service()
    msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    thread_id = msg['threadId']

    thread = service.users().threads().get(userId='me', id=thread_id, format='full').execute()
    messages = thread.get('messages', [])

    full_text = ""
    for m in messages:
        parts = m.get('payload', {}).get('parts', [])
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part.get('body', {}).get('data')
                if data:
                    from base64 import urlsafe_b64decode
                    decoded = urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    full_text += decoded + "\n\n"
    return full_text.strip()
