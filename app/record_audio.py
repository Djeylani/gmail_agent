import sounddevice as sd
import soundfile as sf
from pathlib import Path

def record_audio(filename="voice_note.wav", duration=10, samplerate=44100):
    print(f"🎙️ Recording for {duration} seconds...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    path = Path("recordings") / filename
    path.parent.mkdir(exist_ok=True)
    sf.write(path, audio, samplerate)
    print(f"✅ Saved to {path}")
    return str(path)
