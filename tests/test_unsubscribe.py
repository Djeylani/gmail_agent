from app.email_reader import get_unread_emails
from app.unsubscribe import extract_unsubscribe_links, trigger_unsubscribe

emails = get_unread_emails(max_results=5)

for email in emails:
    print(f"\n📧 {email['from']} — {email['subject']}")
    links = extract_unsubscribe_links(email['id'])
    if links:
        print("🔗 Unsubscribe links found:")
        for link in links:
            print(f"   → {link}")
            trigger_unsubscribe(link)
    else:
        print("❌ No unsubscribe link found.")
