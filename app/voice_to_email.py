import whisper
import datetime
from pathlib import Path

AUDIO_DIR = Path(__file__).parent.parent / "recordings"
AUDIO_DIR.mkdir(exist_ok=True)

model = whisper.load_model("base")

def transcribe_audio(file_path: str) -> str:
    result = model.transcribe(file_path)
    return result["text"]

def format_email_from_transcript(transcript: str, recipient="Unknown", tone="formal") -> dict:
    subject = "Voice Note - " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    body = f"Dear {recipient},\n\n{transcript.strip()}\n\nKind regards,\nDadir"
    return {"to": recipient, "subject": subject, "body": body}
