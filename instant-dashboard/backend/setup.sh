#!/bin/bash

# The Instant Dashboard - Quick Setup Script
# This script helps you set up the application quickly

echo "🚀 The Instant Dashboard - Quick Setup"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo ""
    echo "Please follow these steps:"
    echo "1. Visit https://console.groq.com"
    echo "2. Sign up for a free account"
    echo "3. Create an API key"
    echo "4. Copy the API key"
    echo ""
    read -p "Paste your Groq API key here: " api_key
    
    # Create .env file
    cat > .env << EOF
# Groq API Configuration
GROQ_API_KEY=$api_key

# Model Configuration
GROQ_MODEL=llama-3.3-70b-versatile

# Server Configuration
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173
EOF
    
    echo "✅ Created .env file with your API key"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "📦 Installing Python dependencies..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install dependencies
source venv/bin/activate
pip install -q -r requirements.txt

echo "✅ Backend setup complete!"
echo ""
echo "🎯 Next steps:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python -m app.main"
echo ""
echo "2. In a NEW terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open http://localhost:5173 in your browser"
echo ""
echo "Happy dashboard building! 📊✨"
