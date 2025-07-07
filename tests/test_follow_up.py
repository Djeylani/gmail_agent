from app.follow_up import generate_follow_up

def test_generate_follow_up_reply():
    mock_email = {
        "to": "Fatima",
        "subject": "Re: Collaboration Opportunity"
    }
    reply = generate_follow_up(mock_email, tone="friendly")
    assert "Fatima" in reply
    assert "Just checking in" in reply
