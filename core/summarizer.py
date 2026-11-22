from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.meeting_analyzer import analyze_transcript


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200
    )
    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:
    data = analyze_transcript(transcript)
    return data.get("summary", "No summary available.")


def generate_title(transcript: str) -> str:
    data = analyze_transcript(transcript)
    return data.get("title", "Meeting Discussion")
