# 🎬 AI Video Assistant — Complete Project Summary

## 📌 Project Overview
**AI Video Assistant** is an end-to-end Python application that processes YouTube videos or local video/audio files to automatically **transcribe**, **summarize**, **extract meeting intelligence** (action items, decisions, open questions), and enable **interactive RAG-powered Q&A chat** with the video transcript.

---

## 🏗️ System Architecture & Data Flow

```
                                  ┌────────────────────────┐
                                  │  YouTube URL / Local   │
                                  │   Video & Audio File   │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                                 ┌──────────────────────────┐
                                 │  utils/audio_processor   │
                                 │  (yt-dlp + ffmpeg/pydub) │
                                 └────────────┬─────────────┘
                                              │ Audio Chunks
                                              ▼
                                  ┌────────────────────────┐
                                  │    core/transcriber    │
                                  └───────┬────────┬───────┘
                        English   │        │ Hinglish
                                  ▼        ▼
                           ┌──────────┐  ┌───────────┐
                           │ Whisper  │  │ Sarvam AI │ (Translates to EN)
                           └────┬─────┘  └─────┬─────┘
                                │              │
                                └───────┬──────┘
                                        │ Full Transcript
                                        ▼
             ┌──────────────────────────┼──────────────────────────┐
             │                          │                          │
             ▼                          ▼                          ▼
   ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
   │ core/summarizer  │       │  core/extractor  │       │ core/rag_engine  │
   │  (Mistral LLM)   │       │  (Mistral LLM)   │       │ (ChromaDB + LLM) │
   └─────────┬────────┘       └─────────┬────────┘       └─────────┬────────┘
             │                          │                          │
             ▼                          ▼                          ▼
     Title & Summary           Action Items, Key            Interactive RAG
                               Decisions, Questions           Chat Pipeline
```

---

## 🛠️ Key Components & Directory Structure

```
video_assistent/
├── app.py                      # Streamlit Web UI (High-contrast light theme)
├── main.py                     # CLI Entry Point & interactive terminal chat loop
├── .env                        # Environment keys (MISTRAL_API_KEY, SARVAM_API_KEY)
├── Requirements.txt            # Package dependencies
├── PROJECT_SUMMARY.md          # Project summary and architectural overview
├── core/
│   ├── transcriber.py          # Speech-to-Text routing (Whisper local & Sarvam AI API)
│   ├── summarizer.py           # LLM title & executive summary generation
│   ├── extractor.py            # Extraction of Action Items, Decisions, & Open Questions
│   ├── rag_engine.py           # RAG chain setup (LangChain + Mistral AI + Retriever)
│   └── vector_store.py         # ChromaDB indexing & chunk retrieval
└── utils/
    └── audio_processor.py      # Audio extraction from YouTube/local files & chunking
```

---

## ⚙️ Core Technical Modules

### 1. Dual Speech-to-Text Engines (`core/transcriber.py`)
- **English Transcription**: Uses OpenAI's local `whisper` model (`small` or configurable via `WHISPER_MODEL`).
- **Hinglish/Hindi Translation**: Integrates **Sarvam AI STT** (`saaras:v2.5` / `saaras:v3`). Slices long audio into 25-second 16kHz mono WAV pieces (~800 KB each) with exponential backoff retries to transcribe and translate speech to English simultaneously.

### 2. LLM Intelligence & Structured Extraction (`core/summarizer.py` & `core/extractor.py`)
- Powered by `langchain-mistralai` (`mistral-small-latest`).
- **Title & Summary**: Generates a concise title and executive summary.
- **Action Items**: Extracts tasks, assigned owners, and deadlines.
- **Key Decisions**: Highlights major decisions made during the video/meeting.
- **Open Questions**: Identifies unresolved questions requiring follow-up.

### 3. RAG Q&A Engine (`core/rag_engine.py` & `core/vector_store.py`)
- Indexes transcript chunks into **ChromaDB** using `HuggingFaceEmbeddings` (`sentence-transformers/all-MiniLM-L6-v2`).
- Provides a conversational Q&A chain using **LangChain LCEL** (`RunnablePassthrough`, `ChatPromptTemplate`, `ChatMistralAI`) to answer user questions strictly based on transcript context.

### 4. Audio Processing Pipeline (`utils/audio_processor.py`)
- Downloads audio from YouTube URLs using `yt-dlp` and extracts WAV via `ffmpeg`.
- Converts any local audio/video file format to 16kHz mono WAV using `pydub`.
- Automatically chunks long audio streams into 10-minute segments for memory-efficient processing.

---

## 🚀 Running the Project

### Web Interface (Streamlit)
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser. Enter a YouTube URL or file path, choose your language (`english` or `hinglish`), and click **Analyse**.

### Command Line Interface (CLI)
```bash
python main.py
```
Follow the interactive terminal prompts to process a video and start chatting with the transcript.
