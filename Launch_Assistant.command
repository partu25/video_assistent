#!/bin/bash
# Move to project directory
cd "$(dirname "$0")"

echo "=================================================="
echo "🎬 Starting AI Video Assistant..."
echo "=================================================="

# Check if virtual environment exists
if [ -f "myenv/bin/streamlit" ]; then
    myenv/bin/streamlit run app.py
else
    streamlit run app.py
fi
