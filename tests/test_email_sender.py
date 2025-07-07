def test_send_email_smoke():
    from app.email_sender import send_email
    result = send_email("your-test-email@example.com", "Test Subject", "This is a test.")
    assert "id" in result
