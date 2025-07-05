# Gmail Agent

A Python-based Gmail automation tool that helps manage your inbox with features like reading unread emails and automated unsubscribing.

## Features

- 📧 Read and display unread emails
- 🚫 Automated unsubscribe from mailing lists
- 🔐 Secure OAuth2 authentication with Gmail API
- 🧪 Comprehensive test suite

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Djeylani/gmail_agent.git
   cd gmail_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Google Cloud Setup**
   - Create a project in [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Gmail API
   - Create OAuth2 credentials and download as `credentials.json`
   - Place `credentials.json` in the project root

4. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Configure any additional settings as needed

## Usage

### Reading Unread Emails
```python
from app.email_reader import get_unread_emails

emails = get_unread_emails(max_results=10)
for email in emails:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Snippet: {email['snippet']}")
```

### Unsubscribing from Emails
```python
from app.unsubscribe import extract_unsubscribe_links, trigger_unsubscribe

# Extract unsubscribe links from an email
links = extract_unsubscribe_links(message_id)

# Trigger unsubscribe (opens browser or sends email)
for link in links:
    trigger_unsubscribe(link)
```

## Project Structure

```
gmail_agent/
├── app/
│   ├── __init__.py
│   ├── auth.py          # Gmail API authentication
│   ├── email_reader.py  # Email reading functionality
│   └── unsubscribe.py   # Unsubscribe automation
├── tests/               # Test suite
├── api/                 # API endpoints (future)
├── cli/                 # Command-line interface (future)
├── scheduler/           # Scheduled tasks (future)
└── requirements.txt     # Python dependencies
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Security Notes

- Never commit `credentials.json` or `token.pickle` to version control
- The OAuth app is currently in testing mode with a 100-user limit
- Only authorized test users can access the application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.