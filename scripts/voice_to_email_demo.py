import sys
import argparse
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.record_audio import record_audio
from app.voice_to_email import transcribe_audio
from app.voice_router import interpret_command, compose_email_from_voice

# Parse arguments
parser = argparse.ArgumentParser(description="Voice to Email Demo")
parser.add_argument("--debug", action="store_true", help="Use text input instead of voice")
args = parser.parse_args()

if args.debug:
    # Debug mode: use text input
    transcript = input("📝 Enter your message: ")
    audio_path = None
else:
    # Record and transcribe
    audio_path = record_audio(duration=10)
    transcript = transcribe_audio(audio_path)
    print(f"\n📝 Transcript:\n{transcript}")

# Interpret the command
intent = interpret_command(transcript)
print(f"\n🧭 Detected Intent: {intent}")

# Use voice confirmation flow
if intent == "compose_email":
    compose_email_from_voice(transcript, audio_path or "debug_mode", debug_mode=args.debug)
else:
    print(f"Intent '{intent}' not handled in this demo")

