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
