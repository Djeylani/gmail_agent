import pytest
from app.lead_parser import parse_leads

def test_parse_csv_valid(tmp_path):
    csv_file = tmp_path / "leads.csv"
    csv_file.write_text("name,email,company,notes\nAli,ali@example.com,Barakah Inc.,Interested\n")

    leads = parse_leads(str(csv_file))
    assert len(leads) == 1
    assert leads[0]["email"] == "ali@example.com"

def test_parse_json_valid(tmp_path):
    json_file = tmp_path / "targets.json"
    json_file.write_text('[{"name": "Fatima", "email": "fatima@example.com", "company": "Noor Ltd", "notes": "Follow up"}]')

    leads = parse_leads(str(json_file))
    assert len(leads) == 1
    assert leads[0]["name"] == "Fatima"

def test_invalid_email_filtered(tmp_path):
    csv_file = tmp_path / "leads.csv"
    csv_file.write_text("name,email,company,notes\nZaid,not-an-email,TestCo,Invalid\n")

    leads = parse_leads(str(csv_file))
    assert len(leads) == 0
