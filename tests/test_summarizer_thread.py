from app.email_reader import get_unread_emails, get_thread_text
from app.summarizer import summarize_email

emails = get_unread_emails(max_results=3)

for email in emails:
    print(f"\n📧 {email['from']} — {email['subject']}")
    thread_text = get_thread_text(email['id'])
    if thread_text:
        summary = summarize_email(thread_text)
        print("🧠 Summary:\n", summary)
    else:
        print("⚠️ No thread content found.")
