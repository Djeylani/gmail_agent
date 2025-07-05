import re
import subprocess
import json

def summarize_with_ollama(text, model="mistral"):
    try:
        prompt = f"Summarize the following email thread:\n\n{text}"
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )
        output = result.stdout.decode()
        return output.strip()
    except Exception as e:
        print(f"⚠️ Ollama summarization failed: {e}")
        return None

def summarize_with_regex(text):
    # Simple heuristic: extract first sentence of each paragraph
    paragraphs = text.split("\n\n")
    summary = []
    for para in paragraphs:
        match = re.search(r"([A-Z][^.!?]*[.!?])", para.strip())
        if match:
            summary.append(match.group(1))
    return " ".join(summary)

def summarize_email(text):
    summary = summarize_with_ollama(text)
    if summary:
        return summary
    return summarize_with_regex(text)
