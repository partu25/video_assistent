import whisper
import os
import requests
from pydub import AudioSegment

# Sarvam's sync STT-translate API rejects audio longer than 30s.
# We slice each chunk into 25s pieces (with a 5s safety margin) before sending.
SARVAM_PIECE_SECONDS = 25


WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")


SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")

_model = None


def load_model():

    global _model  

    if _model is None: 
        model_name = os.getenv("WHISPER_MODEL", WHISPER_MODEL)
        print(f"Loading Whisper model: {model_name} ...")
        _model = whisper.load_model(model_name) 
        print("Whisper model loaded.")
    return _model 


def transcribe_chunk_whisper(chunk_path: str) -> str:

    model = load_model()  

    result = model.transcribe(chunk_path, task="transcribe")  
    return result["text"]  


def get_sarvam_api_key() -> str:
    key = os.getenv("SARVAM_API_KEY", "")
    return key.strip().strip('"').strip("'") if key else ""


def _send_to_sarvam(piece_path: str) -> str:
    """Send one ≤30s WAV file to Sarvam and return the English transcript."""
    api_key = get_sarvam_api_key()
    if not api_key:
        raise RuntimeError("SARVAM_API_KEY is not set in environment / .env")

    sarvam_model = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5").strip()

    # Determine endpoint and payload based on configured model version
    if any(m in sarvam_model.lower() for m in ["v3", "v4"]):
        url = "https://api.sarvam.ai/speech-to-text"
        data = {"model": sarvam_model, "mode": "translate"}
    else:
        url = "https://api.sarvam.ai/speech-to-text-translate"
        data = {"model": sarvam_model, "with_diarization": "false"}

    headers = {"api-subscription-key": api_key}
    max_retries = 3

    for attempt in range(1, max_retries + 1):
        try:
            with open(piece_path, "rb") as f:
                files = {"file": (os.path.basename(piece_path), f, "audio/wav")}
                response = requests.post(
                    url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=45,
                )

            if response.ok:
                return response.json().get("transcript", "")

            print(f"\n⚠️ Sarvam attempt {attempt}/{max_retries} returned HTTP {response.status_code}: {response.text}")
            if response.status_code in (429, 500, 502, 503, 504) and attempt < max_retries:
                import time
                time.sleep(2 * attempt)
                continue
            else:
                response.raise_for_status()

        except (requests.exceptions.RequestException, Exception) as e:
            if attempt < max_retries:
                import time
                print(f"⚠️ Sarvam request error on attempt {attempt}/{max_retries}: {e}. Retrying...")
                time.sleep(2 * attempt)
            else:
                print(f"\n❌ Sarvam failed after {max_retries} attempts: {e}")
                raise

    return ""


def transcribe_chunk_sarvam(chunk_path: str) -> str:
    """
    Sarvam sync API only accepts ≤30s audio. We split this chunk into
    25-second pieces (converted to 16kHz Mono for optimal payload size),
    send each separately, and join the transcripts.
    """
    api_key = get_sarvam_api_key()
    if not api_key:
        raise RuntimeError("SARVAM_API_KEY is not set in environment / .env")

    audio = AudioSegment.from_wav(chunk_path)
    piece_ms = SARVAM_PIECE_SECONDS * 1000

    full_text = ""
    total_pieces = (len(audio) + piece_ms - 1) // piece_ms

    for i, start in enumerate(range(0, len(audio), piece_ms)):
        piece = audio[start: start + piece_ms]
        # Convert to 16kHz Mono WAV to optimize payload size (~800KB vs ~4.8MB per 25s)
        piece_mono = piece.set_channels(1).set_frame_rate(16000)

        piece_path = f"{chunk_path}_sv_{i}.wav"
        piece_mono.export(piece_path, format="wav")

        try:
            print(f"  → Sarvam piece {i + 1}/{total_pieces} ...")
            full_text += _send_to_sarvam(piece_path) + " "
        except Exception as err:
            print(f"❌ Error transcribing piece {i + 1}/{total_pieces} with Sarvam: {err}")
        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()

   



def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    """
    Route one chunk to Whisper or Sarvam depending on language choice.
    - english  → Whisper (local model)
    - hinglish → Sarvam (translates to English while transcribing)
    """
    if language.lower() == "hinglish":
        return transcribe_chunk_sarvam(chunk_path)
    return transcribe_chunk_whisper(chunk_path)


def transcribe_all(chunks: list, language: str = "english") -> str:

    full_transcript = "" 

    engine = "Sarvam AI" if language.lower() == "hinglish" else "Whisper"
    print(f"Using {engine} for transcription.")

    for i, chunk in enumerate(chunks):  

        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")

        text = transcribe_chunk(chunk, language=language)  

        full_transcript += text + " "  

    print("Transcription complete.")

    return full_transcript.strip()  