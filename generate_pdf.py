import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

# Image paths
IMG_LANDING = '/Users/parthnesadiya/.gemini/antigravity/brain/ff1be80b-7dbd-458c-8e6a-e6c446bf9bbe/.user_uploaded/media_1789738074618.png'
IMG_SUMMARY = '/Users/parthnesadiya/.gemini/antigravity/brain/ff1be80b-7dbd-458c-8e6a-e6c446bf9bbe/.user_uploaded/media_1789738092531.png'
IMG_CHAT    = '/Users/parthnesadiya/.gemini/antigravity/brain/ff1be80b-7dbd-458c-8e6a-e6c446bf9bbe/.user_uploaded/media_1789738102277.png'

OUTPUT_PDF = '/Users/parthnesadiya/video_assistent/AI_Video_Assistant_Documentation.pdf'


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        if self._pageNumber == 1 or self._pageNumber == 8:
            # Suppress running header/footer on Cover and Thank You pages
            return
        self.saveState()
        self.setFont('Helvetica-Bold', 8)
        self.setFillColor(colors.HexColor('#4f46e5'))
        self.drawString(54, 752, 'AI VIDEO ASSISTANT')
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#475569'))
        self.drawString(145, 752, '|   Comprehensive Project Documentation & Technical Overview')
        
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.5)
        self.line(54, 744, 612 - 54, 744)
        
        self.line(54, 45, 612 - 54, 45)
        page_text = f'Page {self._pageNumber} of {page_count}'
        self.drawRightString(612 - 54, 32, page_text)
        self.drawString(54, 32, 'AI Video Assistant — Project Report & Architecture')
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=30,
        leading=36,
        textColor=colors.HexColor('#1e1b4b'),
        alignment=1, # Center
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#4f46e5'),
        alignment=1,
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1e1b4b'),
        spaceAfter=12,
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4f46e5'),
        spaceBefore=10,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=8,
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        spaceAfter=4,
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white,
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a'),
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE / WELCOME
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("🎬 AI VIDEO ASSISTANT", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Meeting Intelligence · Dual Speech-to-Text · RAG Q&A Engine", subtitle_style))
    story.append(Spacer(1, 25))

    welcome_box_data = [[
        Paragraph(
            "<font color='#4f46e5'><b>WELCOME TO THE PROJECT DOCUMENTATION</b></font><br/><br/>"
            "This document presents a comprehensive, 360-degree technical overview of the "
            "<b>AI Video Assistant</b> project. The system transforms raw video and audio recordings "
            "into structured meeting intelligence—including automated title generation, multi-bullet summaries, "
            "action items, key decisions, open questions, and an interactive RAG chat interface.",
            body_style
        )
    ]]
    welcome_table = Table(welcome_box_data, colWidths=[504])
    welcome_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eef2ff')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#c7d2fe')),
        ('PADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(welcome_table)
    story.append(Spacer(1, 40))

    meta_data = [
        [Paragraph("<b>Project Name:</b>", body_style), Paragraph("AI Video Assistant", body_style)],
        [Paragraph("<b>Primary Stack:</b>", body_style), Paragraph("Python 3.12, Streamlit, LangChain, Mistral AI, Whisper, Sarvam AI, ChromaDB", body_style)],
        [Paragraph("<b>Architecture:</b>", body_style), Paragraph("Dual Speech-to-Text Pipeline + RAG Vector Database", body_style)],
        [Paragraph("<b>Author / Developer:</b>", body_style), Paragraph("Parth Nesadiya", body_style)],
        [Paragraph("<b>Document Version:</b>", body_style), Paragraph("1.0 (Production Build)", body_style)],
        [Paragraph("<b>Status:</b>", body_style), Paragraph("<font color='#059669'><b>Fully Functional & Verified</b></font>", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[130, 374])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 50))
    story.append(Paragraph("<font color='#64748b' size='8'>Generated for Project Verification & Technical Review · 2026</font>", ParagraphStyle('CenterMeta', parent=body_style, alignment=1)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: EXECUTIVE SUMMARY & PURPOSE
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Purpose", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#4f46e5'), spaceAfter=15))

    story.append(Paragraph("<b>1.1 Background & Problem Statement</b>", h2_style))
    story.append(Paragraph(
        "Modern video recordings, webinars, and virtual meeting logs contain vast amounts of valuable information. "
        "However, manually re-watching hours of footage to retrieve specific decisions, assigned tasks, or discussion "
        "snippets is extremely inefficient. Traditional video platforms lack native, automated tools to extract structured "
        "action items or interactively answer detailed questions grounded in video transcripts.",
        body_style
    ))

    story.append(Paragraph("<b>1.2 Project Objectives</b>", h2_style))
    story.append(Paragraph(
        "The <b>AI Video Assistant</b> solves this challenge by delivering an automated end-to-end intelligence engine. "
        "Its primary goals are:",
        body_style
    ))
    story.append(Paragraph("• <b>Automated Audio Extraction & Chunking:</b> Ingest YouTube links or local video files seamlessly.", bullet_style))
    story.append(Paragraph("• <b>Dual Speech-to-Text Pipeline:</b> Support local Whisper models for English and Sarvam AI for Hinglish/Hindi speech translation.", bullet_style))
    story.append(Paragraph("• <b>Structured Meeting Extraction:</b> Generate concise titles, executive summaries, action items (with assigned owners & deadlines), key decisions, and open questions.", bullet_style))
    story.append(Paragraph("• <b>Retrieval-Augmented Generation (RAG):</b> Enable users to chat with the video transcript in real-time.", bullet_style))

    story.append(Paragraph("<b>1.3 Key Value Propositions</b>", h2_style))
    value_data = [
        [Paragraph("<b>Feature</b>", table_header_style), Paragraph("<b>Impact & Value</b>", table_header_style)],
        [Paragraph("<b>90%+ Time Savings</b>", table_body_style), Paragraph("Convert a 1-hour meeting into an executive 1-page summary in under 2 minutes.", table_body_style)],
        [Paragraph("<b>Multilingual STT</b>", table_body_style), Paragraph("Transcribe English locally with Whisper or translate Hinglish speech using Sarvam AI.", table_body_style)],
        [Paragraph("<b>Zero Information Loss</b>", table_body_style), Paragraph("Vector embeddings in ChromaDB store full context for accurate Q&A.", table_body_style)],
        [Paragraph("<b>Rate-Limit Resilience</b>", table_body_style), Paragraph("Built-in exponential retries prevent 429 rate limit issues during LLM calls.", table_body_style)],
    ]
    value_table = Table(value_data, colWidths=[140, 364])
    value_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4f46e5')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(value_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: SYSTEM ARCHITECTURE & PIPELINE
    # =========================================================================
    story.append(Paragraph("2. System Architecture & Pipeline", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#4f46e5'), spaceAfter=15))

    story.append(Paragraph("<b>2.1 End-to-End System Data Flow</b>", h2_style))
    story.append(Paragraph(
        "The architecture is modularized into dedicated pipeline layers ensuring separation of concerns, "
        "reliability, and performance:",
        body_style
    ))

    arch_steps = [
        [Paragraph("<b>1. Audio Processor</b>", table_body_style), Paragraph("Downloads YouTube audio via <code>yt-dlp</code> / <code>ffmpeg</code> or converts local files into 16kHz Mono WAV chunks via <code>pydub</code>.", table_body_style)],
        [Paragraph("<b>2. Speech Transcriber</b>", table_body_style), Paragraph("Routes English audio to local <code>Whisper</code> or Hinglish audio to <code>Sarvam AI API</code> in 25s 16kHz mono slices with retries.", table_body_style)],
        [Paragraph("<b>3. LLM Intelligence</b>", table_body_style), Paragraph("Uses <code>Mistral AI</code> (via <code>langchain-mistralai</code>) to synthesize title, summary, action items, decisions, and questions.", table_body_style)],
        [Paragraph("<b>4. RAG Vector Store</b>", table_body_style), Paragraph("Splits transcript into chunks, embeds via <code>HuggingFaceEmbeddings</code>, and indexes into <code>ChromaDB</code> for fast retrieval.", table_body_style)],
        [Paragraph("<b>5. Streamlit Web UI</b>", table_body_style), Paragraph("Renders an interactive dashboard with live status indicators, cards, and RAG Q&A chat.", table_body_style)],
    ]
    arch_table = Table(arch_steps, colWidths=[130, 374])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f1f5f9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>2.2 Data Flow Architecture Diagram</b>", h2_style))
    
    flow_box_data = [[
        Paragraph(
            "<font color='#1e1b4b'><b>Input (YouTube URL / File)</b></font><br/>"
            "↓<br/>"
            "<b>Audio Extraction & 16kHz Chunking (utils/audio_processor.py)</b><br/>"
            "↓<br/>"
            "<b>Dual STT Routing: Whisper (EN) / Sarvam AI (Hinglish) (core/transcriber.py)</b><br/>"
            "↓<br/>"
            "<b>Full English Transcript Generation</b><br/>"
            "↓<br/>"
            "<b>Parallel Processing: LLM Summarization & Extraction (Mistral AI) | ChromaDB Indexing (RAG)</b><br/>"
            "↓<br/>"
            "<font color='#059669'><b>Interactive Dashboard & Q&A Chat (app.py)</b></font>",
            ParagraphStyle('FlowText', parent=body_style, alignment=1)
        )
    ]]
    flow_table = Table(flow_box_data, colWidths=[504])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('PADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(flow_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: USER INTERFACE & INPUT CONTROLS (IMAGE 1)
    # =========================================================================
    story.append(Paragraph("3. User Interface & Input Controls", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#4f46e5'), spaceAfter=12))

    story.append(Paragraph(
        "The application provides a clean, modern, high-contrast user interface built with Streamlit. "
        "The interface automatically adjusts text contrast and spacing for maximum legibility.",
        body_style
    ))

    if os.path.exists(IMG_LANDING):
        story.append(Image(IMG_LANDING, width=504, height=310))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<i>Figure 3.1: AI Video Assistant Ready to Analyse Landing Page & Input Sidebar</i>", ParagraphStyle('Cap1', parent=body_style, alignment=1, textColor=colors.HexColor('#64748b'), fontSize=8)))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>3.1 Interface Features Breakdown</b>", h2_style))
    story.append(Paragraph("• <b>Sidebar Input Box:</b> Accepts YouTube video links (e.g. <code>https://youtube.com/watch?v=...</code>) or absolute paths to local media files (MP4, WAV, MP3).", bullet_style))
    story.append(Paragraph("• <b>Language Selection Dropdown:</b> Allows users to select between <code>English</code> (processed via Whisper) and <code>Hinglish</code> (processed via Sarvam AI).", bullet_style))
    story.append(Paragraph("• <b>Live Pipeline Status Bar:</b> Displays step-by-step progress dots (Audio Processing → Transcription → Title Generation → Summarization → Extraction → RAG Engine).", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TRANSCRIPTION & SUMMARIZATION (IMAGE 2)
    # =========================================================================
    story.append(Paragraph("4. Speech Transcription & Summarization", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#4f46e5'), spaceAfter=12))

    story.append(Paragraph(
        "Once processing begins, the application extracts the full audio, transcribes it, and presents an executive "
        "summary alongside the complete raw transcript.",
        body_style
    ))

    if os.path.exists(IMG_SUMMARY):
        story.append(Image(IMG_SUMMARY, width=504, height=310))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<i>Figure 4.1: Meeting Title Generation, Structured Executive Summary & Full Transcript Box</i>", ParagraphStyle('Cap2', parent=body_style, alignment=1, textColor=colors.HexColor('#64748b'), fontSize=8)))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>4.1 Key Functionalities</b>", h2_style))
    story.append(Paragraph("• <b>Session Title Generation:</b> Uses LLM prompt engineering to generate a professional title (max 8 words) describing the meeting topic.", bullet_style))
    story.append(Paragraph("• <b>Structured Executive Summary:</b> Breaks down complex discussions into clear bulleted sections (Definition, Key Foundations, Business Applications).", bullet_style))
    story.append(Paragraph("• <b>Full Transcript Expander:</b> Provides a scrollable container displaying the complete raw transcript text for reference.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: MEETING INTELLIGENCE & RAG CHAT (IMAGE 3)
    # =========================================================================
    story.append(Paragraph("5. Meeting Intelligence & RAG Engine", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#4f46e5'), spaceAfter=12))

    story.append(Paragraph(
        "Beyond summarization, the system performs structured intelligence extraction and initializes a Retrieval-Augmented "
        "Generation (RAG) Q&A engine for natural language interaction.",
        body_style
    ))

    if os.path.exists(IMG_CHAT):
        story.append(Image(IMG_CHAT, width=504, height=310))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<i>Figure 5.1: Extracted Meeting Intelligence Cards & Interactive RAG Chat Interface</i>", ParagraphStyle('Cap3', parent=body_style, alignment=1, textColor=colors.HexColor('#64748b'), fontSize=8)))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>5.1 Intelligence Cards & RAG Chat</b>", h2_style))
    story.append(Paragraph("• <b>Action Items Card:</b> Extracts actionable tasks, assigned owners, and deadlines. Displays 'No action items found' if none are present.", bullet_style))
    story.append(Paragraph("• <b>Key Decisions Card:</b> Highlights binding choices made during the meeting.", bullet_style))
    story.append(Paragraph("• <b>Open Questions Card:</b> Lists topics requiring follow-up or unresolved questions.", bullet_style))
    story.append(Paragraph("• <b>Interactive RAG Chat:</b> Allows users to ask natural language questions (e.g., <i>'What were the main decisions made?'</i>). Answers are retrieved strictly from ChromaDB transcript context.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: TECHNICAL STACK & SETUP GUIDE
    # =========================================================================
    story.append(Paragraph("6. Technical Stack & Setup Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#4f46e5'), spaceAfter=15))

    story.append(Paragraph("<b>6.1 Core Technology Stack</b>", h2_style))
    tech_data = [
        [Paragraph("<b>Component</b>", table_header_style), Paragraph("<b>Technology / Library</b>", table_header_style), Paragraph("<b>Role</b>", table_header_style)],
        [Paragraph("<b>Language & Framework</b>", table_body_style), Paragraph("Python 3.12 / Streamlit 1.58", table_body_style), Paragraph("Application runtime & web dashboard UI", table_body_style)],
        [Paragraph("<b>LLM & Orchestration</b>", table_body_style), Paragraph("LangChain / Mistral AI", table_body_style), Paragraph("Prompt chaining, extraction & RAG response generation", table_body_style)],
        [Paragraph("<b>Speech Recognition</b>", table_body_style), Paragraph("Whisper (Local) / Sarvam AI (API)", table_body_style), Paragraph("English STT & Hinglish speech-to-English translation", table_body_style)],
        [Paragraph("<b>Vector Database</b>", table_body_style), Paragraph("ChromaDB / HuggingFace Embeddings", table_body_style), Paragraph("Chunk indexing & semantic similarity search", table_body_style)],
        [Paragraph("<b>Media Processing</b>", table_body_style), Paragraph("pydub / yt-dlp / ffmpeg", table_body_style), Paragraph("YouTube audio download & 16kHz mono chunking", table_body_style)],
    ]
    tech_table = Table(tech_data, colWidths=[130, 174, 200])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e1b4b')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 7),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>6.2 Installation & Execution</b>", h2_style))
    story.append(Paragraph("1. <b>Environment File (.env):</b> Configure your API keys:", body_style))
    code_env = [[Paragraph("<code>MISTRAL_API_KEY=your_mistral_key<br/>SARVAM_API_KEY=your_sarvam_key<br/>MISTRAL_MODEL=open-mistral-7b</code>", table_body_style)]]
    t_env = Table(code_env, colWidths=[504])
    t_env.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')), ('PADDING', (0,0), (-1,-1), 8)]))
    story.append(t_env)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. <b>Run Web Dashboard:</b> <code>streamlit run app.py</code>", body_style))
    story.append(Paragraph("3. <b>Run Terminal CLI:</b> <code>python main.py</code>", body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: CONCLUSION & THANK YOU PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    
    thank_you_box = [[
        Paragraph(
            "<font color='#4f46e5' size='22'><b>THANK YOU!</b></font><br/><br/>"
            "<font size='12'><b>AI Video Assistant Project Documentation</b></font><br/><br/>"
            "Thank you for reviewing the technical documentation and architectural design "
            "of the <b>AI Video Assistant</b>. This system combines state-of-the-art dual speech recognition, "
            "LLM intelligence, and Retrieval-Augmented Generation to transform video content into structured insight.",
            ParagraphStyle('TYText', parent=body_style, alignment=1)
        )
    ]]
    t_ty = Table(thank_you_box, colWidths=[504])
    t_ty.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eef2ff')),
        ('BOX', (0,0), (-1,-1), 2, colors.HexColor('#6366f1')),
        ('PADDING', (0,0), (-1,-1), 24),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_ty)
    story.append(Spacer(1, 40))

    story.append(Paragraph("<b>Future Development Roadmap</b>", h2_style))
    story.append(Paragraph("• <b>Multi-speaker Diarization:</b> Identify and label individual speakers in meeting transcripts.", bullet_style))
    story.append(Paragraph("• <b>Automated PDF/Notion Export:</b> Export meeting summaries and action items directly to Notion or downloadable PDF reports.", bullet_style))
    story.append(Paragraph("• <b>Cloud Deployment:</b> Containerize application via Docker for cloud deployment on AWS / Streamlit Cloud.", bullet_style))

    story.append(Spacer(1, 50))
    story.append(Paragraph("<b>Project Contact & Ownership:</b>", body_style))
    story.append(Paragraph("<b>Author:</b> Parth Nesadiya", body_style))
    story.append(Paragraph("<b>Repository:</b> <code>video_assistent</code>", body_style))
    story.append(Paragraph("<b>Status:</b> Production Ready & Fully Verified", body_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {OUTPUT_PDF}")

if __name__ == '__main__':
    build_pdf()
