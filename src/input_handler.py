"""
Audio input handler for loading and validating audio files.
"""
import soundfile as sf
import numpy as np


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
        # Load audio file with soundfile
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
