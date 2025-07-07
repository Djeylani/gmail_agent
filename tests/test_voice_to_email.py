from app.voice_to_email import format_email_from_transcript

def test_format_email_from_transcript():
    transcript = "Let's schedule a meeting for next Tuesday at 3 PM."
    email = format_email_from_transcript(transcript, recipient="Fatima", tone="formal")
    assert "Fatima" in email["body"]
    assert "meeting" in email["body"]
    assert email["subject"].startswith("Voice Note")
