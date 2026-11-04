import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Uploaded screenshots
IMG_LANDING = '/Users/parthnesadiya/.gemini/antigravity/brain/ff1be80b-7dbd-458c-8e6a-e6c446bf9bbe/.user_uploaded/media_1789738074618.png'
IMG_SUMMARY = '/Users/parthnesadiya/.gemini/antigravity/brain/ff1be80b-7dbd-458c-8e6a-e6c446bf9bbe/.user_uploaded/media_1789738092531.png'
IMG_CHAT    = '/Users/parthnesadiya/.gemini/antigravity/brain/ff1be80b-7dbd-458c-8e6a-e6c446bf9bbe/.user_uploaded/media_1789738102277.png'

OUTPUT_PPTX = '/Users/parthnesadiya/video_assistent/AI_Video_Assistant_Presentation.pptx'

# Colors
C_DARK = RGBColor(0x1E, 0x1B, 0x4B)      # #1e1b4b
C_ACCENT = RGBColor(0x4F, 0x46, 0xE5)    # #4f46e5
C_CYAN = RGBColor(0x08, 0x91, 0xB2)      # #0891b2
C_TEXT = RGBColor(0x0F, 0x17, 0x2A)      # #0f172a
C_MUTED = RGBColor(0x47, 0x55, 0x69)     # #475569
C_BG = RGBColor(0xF8, 0xFA, 0xFC)        # #f8fafc
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)     # #ffffff
C_BORDER = RGBColor(0xCB, 0xD5, 0xE1)    # #cbd5e1


def create_presentation():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="AI VIDEO ASSISTANT"):
        add_bg(slide)
        
        # Top banner line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = C_ACCENT
        line.line.fill.background()

        # Category
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.733), Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_ACCENT
        p.font.name = 'Helvetica'

        # Slide Title
        tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.733), Inches(0.6))
        tf_t = tx_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_DARK
        p_t.font.name = 'Helvetica'

    def add_footer(slide, current_page, total_pages=8):
        tx_f = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.4))
        tf = tx_f.text_frame
        p = tf.paragraphs[0]
        p.text = f"Owner: Bhavya Chaniyara   |   AI Video Assistant Project   |   Slide {current_page} of {total_pages}"
        p.font.size = Pt(9)
        p.font.color.rgb = C_MUTED
        p.font.name = 'Helvetica'

    # =========================================================================
    # SLIDE 1: WELCOME & TITLE COVER SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_bg(slide1)

    # Hero Banner Container
    hero_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    hero_card.fill.solid()
    hero_card.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xFF)
    hero_card.line.color.rgb = RGBColor(0xC7, 0xD2, 0xFE)
    hero_card.line.width = Pt(2)

    tb = slide1.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.333), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "WELCOME TO"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "AI VIDEO ASSISTANT"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "Meeting Intelligence · Dual Speech-to-Text · Interactive RAG Q&A Engine"
    p3.font.size = Pt(16)
    p3.font.color.rgb = C_CYAN
    p3.font.bold = True
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(10)

    p4 = tf.add_paragraph()
    p4.text = "Transforming YouTube links and local video recordings into structured summaries, action items, key decisions, and real-time interactive Q&A."
    p4.font.size = Pt(12)
    p4.font.color.rgb = C_MUTED
    p4.alignment = PP_ALIGN.CENTER
    p4.space_before = Pt(25)

    # Author Card Inside
    p5 = tf.add_paragraph()
    p5.text = "PROJECT OWNER: BHAVYA CHANIYARA"
    p5.font.size = Pt(15)
    p5.font.bold = True
    p5.font.color.rgb = C_DARK
    p5.alignment = PP_ALIGN.CENTER
    p5.space_before = Pt(35)

    p6 = tf.add_paragraph()
    p6.text = "Tech Stack: Python 3.12 | Streamlit | LangChain | Mistral AI | Whisper | Sarvam AI | ChromaDB"
    p6.font.size = Pt(10)
    p6.font.color.rgb = C_MUTED
    p6.alignment = PP_ALIGN.CENTER
    p6.space_before = Pt(8)

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & PROJECT PURPOSE
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Executive Summary & Project Purpose")
    add_footer(slide2, 2)

    # Left Column: Problem & Purpose
    card_l = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = C_WHITE
    card_l.line.color.rgb = C_BORDER

    tb_l = slide2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.6))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Problem Statement & Solution"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    p_body = tf_l.add_paragraph()
    p_body.text = (
        "• Challenge: Re-watching long 1-hour meetings to locate specific decisions or tasks is tedious.\n\n"
        "• Solution: AI Video Assistant automatically ingests YouTube links or local video files, extracts speech, "
        "synthesizes structured intelligence, and answers questions in real-time.\n\n"
        "• Multi-Language Support: Handles English natively and Hinglish/Hindi speech via specialized AI translation."
    )
    p_body.font.size = Pt(12)
    p_body.font.color.rgb = C_TEXT
    p_body.space_before = Pt(10)

    # Right Column: Value Propositions
    card_r = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.0))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = C_WHITE
    card_r.line.color.rgb = C_BORDER

    tb_r = slide2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.333), Inches(4.6))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Key Value Propositions"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    values = [
        ("⚡ 90%+ Time Savings", "Convert 60-minute video meetings into structured bullet points in under 2 minutes."),
        ("🌐 Dual Speech Engine", "Whisper for offline English STT + Sarvam AI for Hinglish speech-to-English translation."),
        ("🧠 Zero Information Loss", "Full transcript indexed in ChromaDB vector store for exact Q&A retrieval."),
        ("🛡️ Rate-Limit Resilience", "Built-in exponential retries prevent 429 rate-limit errors during LLM inference.")
    ]

    for title, desc in values:
        pt = tf_r.add_paragraph()
        pt.text = title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = C_ACCENT
        pt.space_before = Pt(10)

        pd = tf_r.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & PIPELINE
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. System Architecture & Data Flow")
    add_footer(slide3, 3)

    layers = [
        ("1. Audio Processor (utils/audio_processor.py)", "Downloads YouTube audio via yt-dlp/ffmpeg or converts local files into 16kHz Mono WAV chunks via pydub."),
        ("2. Dual Speech Transcriber (core/transcriber.py)", "Routes English to local Whisper STT or Hinglish to Sarvam AI API in 25s 16kHz mono slices with retries."),
        ("3. LLM Intelligence Layer (core/summarizer.py & core/extractor.py)", "Uses Mistral AI (mistral-small-latest / open-mistral-7b) to generate title, summary, action items, decisions, and questions."),
        ("4. RAG Vector Database (core/rag_engine.py & core/vector_store.py)", "Indexes transcript chunks in ChromaDB using HuggingFace embeddings for high-precision vector Q&A retrieval."),
        ("5. Streamlit Dashboard UI (app.py)", "High-contrast web interface with live pipeline status indicators, summary cards, and chat window.")
    ]

    y_start = 1.6
    for i, (title, desc) in enumerate(layers):
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y_start), Inches(11.733), Inches(0.9))
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE if i % 2 == 0 else RGBColor(0xEE, 0xF2, 0xFF)
        card.line.color.rgb = C_BORDER

        tb = slide3.shapes.add_textbox(Inches(1.0), Inches(y_start + 0.05), Inches(11.333), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = C_ACCENT

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_TEXT

        y_start += 1.05

    # =========================================================================
    # SLIDE 4: USER INTERFACE & INPUT CONTROLS (IMAGE 1)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Streamlit User Interface — Input & Controls")
    add_footer(slide4, 4)

    # Left: Image
    if os.path.exists(IMG_LANDING):
        slide4.shapes.add_picture(IMG_LANDING, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.0))

    # Right: Explanatory Box
    card_r = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.733), Inches(5.0))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = C_WHITE
    card_r.line.color.rgb = C_BORDER

    tb_r = slide4.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.333), Inches(4.6))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Interface Highlights"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    features_s4 = [
        ("🎥 Media Input Box", "Paste any YouTube link or enter a local file path (MP4, WAV, MP3)."),
        ("🌐 Language Selection", "Choose English (Whisper) or Hinglish (Sarvam AI translation)."),
        ("⚡ One-Click Analysis", "Click 'Analyse' to trigger audio extraction, chunking, and LLM processing."),
        ("📊 Live Pipeline Tracker", "Sidebar displays step-by-step progress dots (Audio → Transcript → Summary → RAG).")
    ]

    for t_str, d_str in features_s4:
        pt = tf_r.add_paragraph()
        pt.text = t_str
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = C_ACCENT
        pt.space_before = Pt(10)

        pd = tf_r.add_paragraph()
        pd.text = d_str
        pd.font.size = Pt(10)
        pd.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 5: SPEECH TRANSCRIPTION & SUMMARIZATION (IMAGE 2)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Speech Transcription & Executive Summary")
    add_footer(slide5, 5)

    # Left: Image
    if os.path.exists(IMG_SUMMARY):
        slide5.shapes.add_picture(IMG_SUMMARY, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.0))

    # Right: Explanatory Box
    card_r = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.733), Inches(5.0))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = C_WHITE
    card_r.line.color.rgb = C_BORDER

    tb_r = slide5.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.333), Inches(4.6))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Transcription & Summarization"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    features_s5 = [
        ("📌 Meeting Title Generation", "LLM generates a concise, professional session title (max 8 words)."),
        ("📋 Executive Summary", "Map-Reduce LLM prompt chain creates a structured, bulleted meeting breakdown."),
        ("📝 Full Raw Transcript Box", "Scrollable container providing complete transcript text for auditing."),
        ("🎙️ Dual STT Engine", "Whisper runs locally offline; Sarvam AI slices Hinglish audio into 16kHz mono chunks.")
    ]

    for t_str, d_str in features_s5:
        pt = tf_r.add_paragraph()
        pt.text = t_str
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = C_ACCENT
        pt.space_before = Pt(10)

        pd = tf_r.add_paragraph()
        pd.text = d_str
        pd.font.size = Pt(10)
        pd.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 6: MEETING INTELLIGENCE & RAG CHAT (IMAGE 3)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Meeting Intelligence & RAG Q&A Engine")
    add_footer(slide6, 6)

    # Left: Image
    if os.path.exists(IMG_CHAT):
        slide6.shapes.add_picture(IMG_CHAT, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.0))

    # Right: Explanatory Box
    card_r = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.6), Inches(4.733), Inches(5.0))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = C_WHITE
    card_r.line.color.rgb = C_BORDER

    tb_r = slide6.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.333), Inches(4.6))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Intelligence Cards & RAG"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    features_s6 = [
        ("✅ Action Items Card", "Extracts actionable tasks, assigned owners, and deadlines."),
        ("🔑 Key Decisions Card", "Highlights major binding choices agreed upon during the session."),
        ("❓ Open Questions Card", "Identifies unresolved topics needing follow-up."),
        ("💬 Interactive RAG Chat", "Ask natural language questions. Answers are retrieved directly from ChromaDB context.")
    ]

    for t_str, d_str in features_s6:
        pt = tf_r.add_paragraph()
        pt.text = t_str
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = C_ACCENT
        pt.space_before = Pt(10)

        pd = tf_r.add_paragraph()
        pd.text = d_str
        pd.font.size = Pt(10)
        pd.font.color.rgb = C_TEXT

    # =========================================================================
    # SLIDE 7: TECHNICAL STACK & SETUP GUIDE
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Technical Stack & Setup Guide")
    add_footer(slide7, 7)

    # Left Column: Tech Stack Table
    card_l = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = C_WHITE
    card_l.line.color.rgb = C_BORDER

    tb_l = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.6))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "Technology Stack"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    tech_list = [
        ("Framework & UI:", "Python 3.12 / Streamlit 1.58"),
        ("LLM & RAG Chaining:", "LangChain / Mistral AI"),
        ("Speech Recognition:", "Whisper (Local) & Sarvam AI (API)"),
        ("Vector DB:", "ChromaDB / HuggingFace Embeddings"),
        ("Media Processing:", "pydub / yt-dlp / ffmpeg")
    ]

    for k, v in tech_list:
        pt = tf_l.add_paragraph()
        pt.text = k
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = C_ACCENT
        pt.space_before = Pt(8)

        pd = tf_l.add_paragraph()
        pd.text = v
        pd.font.size = Pt(11)
        pd.font.color.rgb = C_TEXT

    # Right Column: Commands
    card_r = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.0))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = C_WHITE
    card_r.line.color.rgb = C_BORDER

    tb_r = slide7.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.333), Inches(4.6))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Execution Commands"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    cmd_list = [
        ("1. Configure .env File", "MISTRAL_API_KEY=your_key\nSARVAM_API_KEY=your_key\nMISTRAL_MODEL=open-mistral-7b"),
        ("2. Launch Web Dashboard", "streamlit run app.py"),
        ("3. Launch Terminal CLI", "python main.py")
    ]

    for k, v in cmd_list:
        pt = tf_r.add_paragraph()
        pt.text = k
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = C_ACCENT
        pt.space_before = Pt(12)

        pd = tf_r.add_paragraph()
        pd.text = v
        pd.font.size = Pt(11)
        pd.font.name = 'Courier'
        pd.font.color.rgb = C_DARK

    # =========================================================================
    # SLIDE 8: THANK YOU SLIDE
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_bg(slide8)

    ty_card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    ty_card.fill.solid()
    ty_card.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xFF)
    ty_card.line.color.rgb = RGBColor(0x63, 0x66, 0xF1)
    ty_card.line.width = Pt(2)

    tb = slide8.shapes.add_textbox(Inches(1.5), Inches(1.4), Inches(10.333), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "THANK YOU!"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = C_ACCENT
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "AI Video Assistant Project Presentation"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "Thank you for reviewing the project presentation and technical architecture."
    p3.font.size = Pt(13)
    p3.font.color.rgb = C_MUTED
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(15)

    p4 = tf.add_paragraph()
    p4.text = "PRESENTED & OWNED BY: BHAVYA CHANIYARA"
    p4.font.size = Pt(16)
    p4.font.bold = True
    p4.font.color.rgb = C_DARK
    p4.alignment = PP_ALIGN.CENTER
    p4.space_before = Pt(35)

    p5 = tf.add_paragraph()
    p5.text = "Project Status: Fully Functional, Verified & Production Ready"
    p5.font.size = Pt(12)
    p5.font.bold = True
    p5.font.color.rgb = RGBColor(0x05, 0x96, 0x69)
    p5.alignment = PP_ALIGN.CENTER
    p5.space_before = Pt(10)

    prs.save(OUTPUT_PPTX)
    print(f"PowerPoint Presentation successfully saved to: {OUTPUT_PPTX}")

if __name__ == '__main__':
    create_presentation()
