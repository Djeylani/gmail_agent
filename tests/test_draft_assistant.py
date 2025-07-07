import pytest
from app.draft_assistant import generate_reply

def test_halal_filter_blocks_sensitive_reply():
    context = {
        "name": "Ali",
        "subject": "Weekend Plan",
        "topic": "Wine tasting",
        "body": "Let's meet at the wine bar after work."
    }

    with pytest.raises(ValueError) as exc_info:
        generate_reply("reply_spiritual.j2", context, strict_halal=True)

    assert "non-halal content" in str(exc_info.value)


def test_halal_filter_allows_clean_reply():
    context = {
        "name": "Fatima",
        "subject": "Collaboration Opportunity",
        "topic": "ethical AI",
        "body": "I'd love to explore how our work might align and benefit the ummah."
    }

    email = generate_reply("reply_spiritual.j2", context, strict_halal=True)
    assert "Fatima" in email
    assert "ethical AI" in email