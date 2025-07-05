from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

service = build('gmail', 'v1', credentials=creds)
results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
messages = results.get('messages', [])

print(f"You have {len(messages)} unread emails.")
