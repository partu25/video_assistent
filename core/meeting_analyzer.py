import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.llm_factory import get_llm, invoke_with_retry

# In-memory cache to ensure unified analysis runs exactly once per transcript
_ANALYSIS_CACHE = {}


def analyze_transcript(transcript: str) -> dict:
    """
    Runs a single comprehensive analysis call to extract Title, Summary,
    Action Items, Key Decisions, and Open Questions simultaneously.
    
    This reduces API calls from 5-10 requests down to 1 single request,
    preventing HTTP 429 Rate Limit Exceeded errors on Mistral API free tiers.
    """
    if not transcript or not transcript.strip():
        return {
            "title": "No Transcript Provided",
            "summary": "Transcript is empty.",
            "action_items": "No action items found.",
            "key_decisions": "No key decisions found.",
            "open_questions": "No open questions found."
        }

    # Cache key based on length and hash
    cache_key = (len(transcript), hash(transcript.strip()))
    if cache_key in _ANALYSIS_CACHE:
        return _ANALYSIS_CACHE[cache_key]

    llm = get_llm(temperature=0.2)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert meeting analyst. Analyze the provided meeting transcript thoroughly and return your entire analysis formatted EXACTLY using the following section delimiters:

===TITLE===
(Provide a concise, professional session title, maximum 8 words, without quotation marks)

===SUMMARY===
(Provide a comprehensive executive summary in clear markdown bullet points covering main topics, discussion points, and key outcomes)

===ACTION_ITEMS===
(Provide a numbered list of action items. For each item provide:
- Task description
- Owner (who is responsible)
- Deadline (if mentioned, else write 'Not specified')
If none found, write 'No action items found.')

===KEY_DECISIONS===
(Provide a numbered list of key decisions made. If none found, write 'No key decisions found.')

===OPEN_QUESTIONS===
(Provide a numbered list of unresolved questions or topics needing follow-up. If none found, write 'No open questions found.')
"""
        ),
        ("human", "{text}")
    ])

    chain = prompt | llm | StrOutputParser()

    # Limit to first 40,000 characters to stay safely within token context
    input_text = transcript[:40000] if len(transcript) > 40000 else transcript
    raw_output = invoke_with_retry(chain, {"text": input_text})

    sections = {
        "title": "Meeting Analysis",
        "summary": "No summary generated.",
        "action_items": "No action items found.",
        "key_decisions": "No key decisions found.",
        "open_questions": "No open questions found."
    }

    pattern = r"===([A-Z_]+)===\s*\n(.*?)(?=(?:===[A-Z_]+===|\Z))"
    matches = re.findall(pattern, raw_output, re.DOTALL)
    for tag, content in matches:
        k = tag.lower()
        if k in sections:
            cleaned = content.strip().strip("---").strip()
            if cleaned:
                # Clean up title if wrapped in quotes or markdown bold
                if k == "title":
                    cleaned = cleaned.replace('"', '').replace('**', '').strip()
                sections[k] = cleaned

    _ANALYSIS_CACHE[cache_key] = sections
    return sections
