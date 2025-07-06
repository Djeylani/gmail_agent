import csv
import json
import re
from pathlib import Path

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_email(email):
    return EMAIL_REGEX.match(email) is not None

def parse_csv(file_path):
    leads = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row.get("email", "").strip()
            if is_valid_email(email):
                leads.append({
                    "name": row.get("name", "").strip(),
                    "email": email,
                    "company": row.get("company", "").strip(),
                    "notes": row.get("notes", "").strip()
                })
    return leads

def parse_json(file_path):
    leads = []
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
        for entry in data:
            email = entry.get("email", "").strip()
            if is_valid_email(email):
                leads.append({
                    "name": entry.get("name", "").strip(),
                    "email": email,
                    "company": entry.get("company", "").strip(),
                    "notes": entry.get("notes", "").strip()
                })
    return leads

def parse_leads(file_path):
    path = Path(file_path)
    if path.suffix == ".csv":
        return parse_csv(file_path)
    elif path.suffix == ".json":
        return parse_json(file_path)
    else:
        raise ValueError("Unsupported file format. Use .csv or .json")
