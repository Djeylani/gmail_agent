from app.auth import get_gmail_service

service = get_gmail_service()
profile = service.users().getProfile(userId='me').execute()
print(f"Authenticated as: {profile['emailAddress']}")
# This code tests the authentication process with Gmail API and prints the authenticated user's email address.