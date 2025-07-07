from app.content_filter import scan_text, is_halal

def test_detects_sensitive_terms():
    text = "This email mentions alcohol and gambling."
    matches = scan_text(text)
    assert "alcohol" in matches
    assert "gambling" in matches
    assert not is_halal(text)

def test_passes_clean_text():
    text = "Looking forward to collaborating on ethical AI projects."
    matches = scan_text(text)
    assert matches == []
    assert is_halal(text)
