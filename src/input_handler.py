"""
Audio input handler for loading and validating audio files.
"""
import soundfile as sf
import numpy as np
import tempfile
import os
from pathlib import Path
from pydub import AudioSegment


def load_audio(file_path: str, max_duration: int = 360) -> tuple[np.ndarray, int]:
    """
    Load an audio file and return the audio signal and sample rate.
    
    Args:
        file_path: Path to the audio file
        max_duration: Maximum duration in seconds (default: 360 = 6 minutes)
    
    Returns:
        tuple: (audio_signal, sample_rate)
    
    Raises:
        FileNotFoundError: If the audio file doesn't exist
        ValueError: If the audio file exceeds the maximum duration
    """
    try:
        file_extension = Path(file_path).suffix.lower()
        
        # Handle M4A files by converting to WAV temporarily
        if file_extension == '.m4a':
            print("Converting M4A file...")
            audio_segment = AudioSegment.from_file(file_path, format='m4a')
            
            # Create a temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                tmp_wav_path = tmp_file.name
                audio_segment.export(tmp_wav_path, format='wav')
            
            try:
                # Load the temporary WAV file
                audio, sample_rate = sf.read(tmp_wav_path, dtype='float32')
            finally:
                # Clean up temporary file
                os.unlink(tmp_wav_path)
        else:
            # Load audio file with soundfile for other formats
            audio, sample_rate = sf.read(file_path, dtype='float32')
        
        # Convert to mono if stereo
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        
        # Check duration
        duration = len(audio) / sample_rate
        if duration > max_duration:
            raise ValueError(
                f"Audio file duration ({duration:.1f}s) exceeds maximum "
                f"allowed duration ({max_duration}s)"
            )
        
        print(f"Loaded audio: {file_path}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Sample rate: {sample_rate} Hz")
        
        return audio, sample_rate
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error loading audio file: {str(e)}")
