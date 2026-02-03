# Spectrogrammer

A simple Python application that generates spectrograms from audio files in the time-frequency domain. The maximum length of the audio files is 6 minutes.

## Installation

### Windows

1. Download or clone this repository
2. Double-click `install.bat` or run it in Command Prompt
3. The script will automatically:
   - Download and install Python 3.12 if not present
   - Create a virtual environment
   - Install all required dependencies

After installation, to use the program:
```cmd
venv\Scripts\activate.bat
venv\Scripts\python.exe src\main.py <path\to\your\audio.wav>
```

### macOS / Linux

1. Download or clone this repository
2. Open Terminal and navigate to the project folder
3. Run the installation script:
```bash
./install.sh
```
4. The script will automatically:
   - Install Homebrew (if needed)
   - Install Python 3 (if needed)
   - Create a virtual environment
   - Install all required dependencies

After installation, to use the program:
```bash
source venv/bin/activate
venv\Scripts\python.exe src\main.py <path\to\your\audio.wav>
```

### Manual Installation

If you prefer to install manually or already have Python installed:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage (display spectrogram):
```bash
venv\Scripts\python.exe src\main.py <path\to\your\audio.wav>
```

Save spectrogram to a file:
```bash
venv\Scripts\python.exe src\main.py <path\to\your\audio.wav> -o <path\to\spectrogram_image.png>
```

Save without displaying:
```bash
venv\Scripts\python.exe src\main.py <path\to\your\audio.wav> -o <path\to\spectrogram_image.png> --no-show
```

## Supported Audio Formats

The application supports various audio formats including:
- WAV
- MP3
- FLAC
- OGG
- M4A