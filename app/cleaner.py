from app.auth import get_gmail_service

def get_matching_emails(query, max_results=100):
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    return results.get('messages', [])

def delete_email(message_id):
    service = get_gmail_service()
    service.users().messages().trash(userId='me', id=message_id).execute()

def clean_inbox():
    rules = [
        {"label": "🧠 CPU Alerts", "query": 'subject:"CPU Alert" to:me'},
        {"label": "🧪 VirusTotal Alerts", "query": 'subject:"VirusTotal Alert" to:me'},
        {"label": "📤 Self-sent", "query": 'from:me to:me'},
        {"label": "📢 Newsletters", "query": 'from:(newsletter@ OR no-reply@)'},
        {"label": "🗑️ Unwanted Label", "query": 'label:Unwanted'},
        {"label": "🚫 Unsubscribed Label", "query": 'label:Unsubscribed'},
        {"label": "📭 Unread Inbox", "query": 'is:unread in:inbox'},
    ]

    for rule in rules:
        print(f"\n🔍 Cleaning: {rule['label']}")
        messages = get_matching_emails(rule["query"])
        if not messages:
            print("✅ Nothing to delete.")
            continue
        for msg in messages:
            try:
                delete_email(msg["id"])
                print(f"🗑️ Trashed message {msg['id']}")
            except Exception as e:
                print(f"❌ Failed to delete {msg['id']}: {e}")

    print("\n✅ Inbox cleanup complete.")
