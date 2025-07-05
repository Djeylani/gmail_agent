from app.email_reader import get_unread_emails  # ✅ Make sure this matches the function name

emails = get_unread_emails()
for email in emails:
    print(f"📧 {email['from']} — {email['subject']}")
    print(f"    {email['snippet']}\n")
