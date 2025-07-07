import datetime
from app.email_reader import get_sent_emails, get_thread_replies
from app.draft_assistant import generate_reply
from app.auth import get_gmail_service
from app.email_sender import send_email  # assumes you have this module


def find_threads_needing_follow_up(days=3):
    """
    Return a list of sent threads with no reply after `days` days.
    """
    sent_emails = get_sent_emails()
    threshold = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    threads_to_follow_up = []

    for email in sent_emails:
        thread_id = email.get("threadId")
        sent_time = datetime.datetime.fromtimestamp(int(email["internalDate"]) / 1000)

        if sent_time < threshold:
            replies = get_thread_replies(thread_id)
            if not replies:
                threads_to_follow_up.append(email)

    return threads_to_follow_up

def generate_follow_up(email, tone="friendly"):
    context = {
        "name": email.get("to", "there"),
        "subject": email.get("subject", "Following up"),
        "topic": "our previous conversation",
        "body": "Just checking in to see if you had a chance to review my last message."
    }
    return generate_reply(f"reply_{tone}.j2", context)


def send_follow_up(email, reply_text):
    to = email.get("to")
    subject = f"Re: {email.get('subject', 'Following up')}"
    send_email(to=to, subject=subject, body=reply_text)
