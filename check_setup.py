import sys
import shutil
import os

def check():
    print("=" * 60)
    print("🎬 AI Video Assistant — Environment Pre-Flight Check")
    print("=" * 60)
    all_ok = True

    # 1. Python Version Check
    v = sys.version_info
    print(f"1. Python Version: {v.major}.{v.minor}.{v.micro}", end=" ")
    if v.major == 3 and v.minor >= 10:
        print("✅ OK")
    else:
        print("❌ WARNING (Python 3.10+ recommended)")
        all_ok = False

    # 2. FFmpeg Binary Check
    ffmpeg_path = shutil.which("ffmpeg")
    print(f"2. FFmpeg Audio Converter:", end=" ")
    if ffmpeg_path:
        print(f"✅ Found ({ffmpeg_path})")
    else:
        print("❌ NOT FOUND")
        print("   👉 Fix: Install FFmpeg on your system:")
        print("      - macOS: brew install ffmpeg")
        print("      - Windows: winget install Gyan.FFmpeg  (or choco install ffmpeg)")
        print("      - Linux: sudo apt update && sudo apt install ffmpeg")
        all_ok = False

    # 3. .env File Check
    print("3. .env Configuration File:", end=" ")
    if os.path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()
        g_key = os.getenv("GROQ_API_KEY", "").strip()
        m_key = os.getenv("MISTRAL_API_KEY", "").strip()
        s_key = os.getenv("SARVAM_API_KEY", "").strip()
        if (g_key or m_key) and s_key:
            provider = "Groq" if g_key else "Mistral"
            print(f"✅ Configured with API Keys (LLM: {provider})")
        else:
            print("⚠️ .env exists but LLM key (GROQ_API_KEY or MISTRAL_API_KEY) or SARVAM_API_KEY is missing!")
            all_ok = False
    else:
        print("❌ Missing .env file!")
        print("   👉 Fix: Create a .env file with:")
        print("      GROQ_API_KEY=your_groq_key")
        print("      SARVAM_API_KEY=your_sarvam_key")
        all_ok = False

    # 4. Package Import Check
    print("4. Python Libraries Check:", end=" ")
    packages = [
        ("streamlit", "streamlit"),
        ("langchain", "langchain"),
        ("langchain_mistralai", "langchain-mistralai"),
        ("whisper", "openai-whisper"),
        ("pydub", "pydub"),
        ("yt_dlp", "yt-dlp"),
        ("chromadb", "chromadb"),
    ]
    missing = []
    for mod, pkg in packages:
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)

    if not missing:
        print("✅ All Core Packages Installed")
    else:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("   👉 Fix: Run: pip install -r Requirements.txt")
        all_ok = False

    print("=" * 60)
    if all_ok:
        print("🎉 SUCCESS: Your friend's laptop is 100% READY!")
        print("👉 Run: streamlit run app.py")
    else:
        print("⚠️ Please resolve the items marked with ❌ above before running.")
    print("=" * 60)

if __name__ == "__main__":
    check()
