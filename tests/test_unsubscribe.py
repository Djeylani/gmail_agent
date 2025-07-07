import pytest
from app.email_reader import get_unread_emails
from app.unsubscribe import (
    extract_unsubscribe_links,
    trigger_unsubscribe,
    archive_and_label_message
)

def test_unsubscribe_flow():
    emails = get_unread_emails(max_results=1)

    if not emails:
        pytest.skip("No unread emails available for unsubscribe test.")

    for email in emails:
        assert "from" in email
        assert "subject" in email
        assert "id" in email

        links = extract_unsubscribe_links(email["id"])
        if links:
            for link in links:
                trigger_unsubscribe(link)
            archive_and_label_message(email["id"])