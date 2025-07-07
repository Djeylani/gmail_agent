def interpret_command(transcript: str) -> str:
    transcript = transcript.lower()

    if "follow up" in transcript:
        return "follow_up"
    elif "unsubscribe" in transcript:
        return "unsubscribe"
    elif "summarize" in transcript:
        return "summarize"
    elif "send email" in transcript or "compose" in transcript:
        return "compose_email"
    else:
        return "unknown"
