from rapidfuzz import process

CONTACTS = {
    "fatima": "fatima@example.com",
    "ali": "ali@startuphub.org",
    "dees": "deesthought@gmail.com",
    "d": "deesthought@gmail.com",
    "john": "john.doe@gmail.com",
    "sarah": "sarah.smith@outlook.com",
    "mike": "mike.johnson@yahoo.com",
    "lisa": "lisa.brown@hotmail.com",
    "david": "david.wilson@gmail.com",
    "emma": "emma.davis@protonmail.com",
    "alex": "alex.taylor@icloud.com",
    "maria": "maria.garcia@gmail.com",
    "tom": "tom.anderson@outlook.com",
    "anna": "anna.martinez@yahoo.com"
}

def add_contact(name: str, email: str):
    """Adds a new contact to the CONTACTS dictionary."""
    CONTACTS[name.lower()] = email.lower()

def resolve_contact(name: str, threshold=80) -> str | None:
    name = name.lower().strip()
    match, score, _ = process.extractOne(name, CONTACTS.keys())
    if score >= threshold:
        return CONTACTS[match]
    return None
