import re

# Define patterns to flag non-halal or sensitive content
SENSITIVE_PATTERNS = [
    r"\b(alcohol|beer|wine|vodka|whiskey)\b",
    r"\b(gambling|casino|betting|lottery)\b",
    r"\b(pork|bacon|ham|pepperoni)\b",
    r"\b(nudity|explicit|adult content|NSFW)\b",
    r"\b(interest\s+rate|APR|loan shark)\b",
    r"\b(crypto\s+scam|get rich quick|forex scheme)\b",
]

def scan_text(text: str) -> list:
    """
    Scan the input text for sensitive patterns.
    Returns a list of matched terms.
    """
    matches = []
    for pattern in SENSITIVE_PATTERNS:
        found = re.findall(pattern, text, re.IGNORECASE)
        matches.extend(found)
    return matches

def is_halal(text: str) -> bool:
    """
    Returns True if no sensitive content is found.
    """
    return len(scan_text(text)) == 0