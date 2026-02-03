#!/bin/bash

echo "======================================"
echo "Spectrogrammer Installation Script"
echo "======================================"
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✓ Homebrew is already installed"
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Installing Python 3..."
    brew install python3
else
    echo "✓ Python 3 is already installed"
    python3 --version
fi

# Check if ffmpeg is installed (required for M4A support)
if ! command -v ffmpeg &> /dev/null; then
    echo "ffmpeg not found. Installing ffmpeg (required for M4A support)..."
    brew install ffmpeg
else
    echo "✓ ffmpeg is already installed"
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "======================================"
echo "Installation complete!"
echo "======================================"
echo ""
echo "To use Spectrogrammer:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo "  2. Run the program:"
echo "     python src/main.py path/to/audio.wav"
echo ""
echo "Supported formats: WAV, MP3, FLAC, OGG, M4A"
echo ""
