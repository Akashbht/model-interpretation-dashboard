#!/bin/bash

# Model Interpretation Dashboard Startup Script

echo "🚀 Starting Model Interpretation Dashboard..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip and try again."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please run this script from the project directory."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Please check your Python/pip installation."
    exit 1
fi

echo "✅ Dependencies installed successfully!"
echo

# Run tests
echo "🧪 Running validation tests..."
python3 test_dashboard.py

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please check the error messages above."
    exit 1
fi

echo "✅ All tests passed!"
echo

# Start the dashboard
echo "🎉 Starting the dashboard..."
echo "📍 The dashboard will open at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the dashboard"
echo

streamlit run app.py