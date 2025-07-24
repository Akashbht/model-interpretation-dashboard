#!/bin/bash

echo "Model Interpretation Dashboard - Development Setup"
echo "=================================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your API keys before running the application."
fi

# Setup backend
echo "Setting up backend..."
cd backend

# Install Python dependencies
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "Backend setup complete!"
cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend

# Install Node.js dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

echo "Frontend setup complete!"
cd ..

echo ""
echo "Setup complete! To start the application:"
echo "1. Edit .env file with your API keys"
echo "2. Start backend: cd backend && source venv/bin/activate && python app.py"
echo "3. Start frontend: cd frontend && npm start"
echo ""
echo "The dashboard will be available at http://localhost:3000"