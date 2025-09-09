#!/bin/bash

# Setup script for GCP Speech Translation Pipeline

echo "🚀 Setting up GCP Speech Translation Pipeline"
echo "=============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🔧 Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Set up GCP authentication:"
echo "   - Copy .env.example to .env"
echo "   - Update .env with your GCP credentials path"
echo "   - Or set environment variable:"
echo "     export GOOGLE_APPLICATION_CREDENTIALS='/path/to/your/key.json'"
echo ""
echo "3. Run the demo:"
echo "   python demo.py"
echo ""
echo "4. Process an audio file:"
echo "   python main.py your_audio.wav"
echo ""
echo "📖 For more information, see README.md"