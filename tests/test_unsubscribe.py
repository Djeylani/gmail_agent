from app.email_reader import get_unread_emails
from app.unsubscribe import (
    extract_unsubscribe_links,
    trigger_unsubscribe,
    archive_and_label_message
)

def test_unsubscribe_flow():
    emails = get_unread_emails(max_results=1)

    assert isinstance(emails, list)
    assert len(emails) > 0

    for email in emails:
        assert "from" in email
        assert "subject" in email
        assert "id" in email

        print(f"\n📧 {email['from']} — {email['subject']}")
        links = extract_unsubscribe_links(email['id'])

        if links:
            print("🔗 Unsubscribe links found:")
            for link in links:
                print(f"   → {link}")
                try:
                    trigger_unsubscribe(link)
                except Exception as e:
                    print(f"⚠️ Failed to unsubscribe: {e}")
            archive_and_label_message(email['id'])
        else:
            print("❌ No unsubscribe link found.")
