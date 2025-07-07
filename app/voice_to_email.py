import whisper
import datetime
import os
from pathlib import Path

AUDIO_DIR = Path(__file__).parent.parent / "recordings"
AUDIO_DIR.mkdir(exist_ok=True)

# Add common FFmpeg paths to environment
ffmpeg_paths = [
    r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin",
    r"C:\Program Files\Krita (x64)\bin",
    r"C:\Users\User\AppData\Local\Microsoft\WinGet\Links"
]

for path in ffmpeg_paths:
    if os.path.exists(path) and path not in os.environ.get('PATH', ''):
        os.environ['PATH'] = path + os.pathsep + os.environ.get('PATH', '')
        break

model = whisper.load_model("base")

def transcribe_audio(file_path: str, language="en") -> str:
    try:
        result = model.transcribe(file_path, language=language, fp16=False)
        return result["text"]
    except FileNotFoundError as e:
        print(f"Error: FFmpeg not found. {e}")
        return ""

def format_email_from_transcript(transcript: str, recipient="Unknown", tone="formal") -> dict:
    subject = "Voice Note - " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    body = f"Dear {recipient},\n\n{transcript.strip()}\n\nKind regards,\nDadir"
    return {"to": recipient, "subject": subject, "body": body}
