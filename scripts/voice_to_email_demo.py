import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.record_audio import record_audio
from app.voice_to_email import transcribe_audio, format_email_from_transcript
from app.email_sender import send_email
from app.voice_router import interpret_command

# Record
audio_path = record_audio(duration=10)

# Transcribe
transcript = transcribe_audio(audio_path)
print(f"\n📝 Transcript:\n{transcript}")

# Format
email = format_email_from_transcript(transcript, recipient="Fatima")
print(f"\n📧 Formatted Email:\nTo: {email['to']}\nSubject: {email['subject']}\n\n{email['body']}")


# Step 4: Send the email
send_email(to="deesthought@gmail.com", subject=email["subject"], body=email["body"])
print("✅ Email sent to deesthought@gmail.com")

# Step 5: Interpret the command
intent = interpret_command(transcript)
print(f"\n🧭 Detected Intent: {intent}")

