from app.summarizer import summarize_email

sample_email = """
Hi team,

Just a quick update on the project status. We've completed the backend integration and are now testing the API endpoints.

Next steps:
- Finalize frontend components
- Conduct user testing
- Prepare for deployment

Let me know if you have any questions.

Best,
Dadir
"""

summary = summarize_email(sample_email)
print("🧠 Summary:\n", summary)
