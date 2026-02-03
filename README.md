# Spectrogrammer

A simple Python application that generates spectrograms from audio files in the time-frequency domain.

## Features

- Load audio files up to 6 minutes long
- Generate spectrogram using Short-Time Fourier Transform (STFT)
- Visualize the time-frequency representation
- Save spectrogram as an image file

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage (display spectrogram):
```bash
python main.py path/to/your/audio.wav
```

Save spectrogram to a file:
```bash
python main.py path/to/your/audio.wav -o spectrogram.png
```

Save without displaying:
```bash
python main.py path/to/your/audio.wav -o spectrogram.png --no-show
```

## Project Structure

- `main.py` - Main application entry point with command-line interface
- `input_handler.py` - Handles audio file loading and validation
- `spectrogram_processor.py` - Generates and plots spectrograms
- `requirements.txt` - Python package dependencies

## Supported Audio Formats

The application supports various audio formats including:
- WAV
- MP3
- FLAC
- OGG
- M4A

## Technical Details

- Uses **librosa** for audio processing and STFT computation
- Uses **matplotlib** for visualization
- Maximum audio duration: 6 minutes (360 seconds)
- Spectrogram displayed in dB scale with time and frequency axes
