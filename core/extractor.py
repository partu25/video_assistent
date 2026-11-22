# Action items, key decisions, and open questions extraction
from core.meeting_analyzer import analyze_transcript


def extract_action_items(transcript: str) -> str:
    data = analyze_transcript(transcript)
    return data.get("action_items", "No action items found.")


def extract_key_decisions(transcript: str) -> str:
    data = analyze_transcript(transcript)
    return data.get("key_decisions", "No key decisions found.")


def extract_questions(transcript: str) -> str:
    data = analyze_transcript(transcript)
    return data.get("open_questions", "No open questions found.")
