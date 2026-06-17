#!/bin/bash
# FinWiz Journal - Quick Start Script for macOS/Linux

echo ""
echo "========================================"
echo "  FinWiz Journal - Starting..."
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment."
        echo "Make sure Python 3 is installed."
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error activating virtual environment."
    exit 1
fi

# Install/update dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies."
    exit 1
fi

# Run Streamlit app
echo ""
echo "Starting FinWiz Journal..."
echo ""
echo "The app will open at: http://localhost:8501"
echo ""

streamlit run app.py
