"""
Spectrogram processing and visualization module.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def generate_spectrogram(audio: np.ndarray, sample_rate: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate a spectrogram from an audio signal.
    
    Args:
        audio: Audio signal as numpy array
        sample_rate: Sample rate of the audio
    
    Returns:
        tuple: (frequencies, times, spectrogram in dB scale)
    """
    # Compute Short-Time Fourier Transform (STFT)
    frequencies, times, stft = signal.spectrogram(audio, fs=sample_rate, nperseg=2048)
    
    # Convert to dB scale
    spectrogram_db = 10 * np.log10(stft + 1e-10)
    
    return frequencies, times, spectrogram_db


def plot_spectrogram(frequencies: np.ndarray, times: np.ndarray, 
                     spectrogram: np.ndarray, output_path: str = None, show: bool = True):
    """
    Plot and optionally save a spectrogram.
    
    Args:
        frequencies: Frequency bins
        times: Time bins
        spectrogram: Magnitude spectrogram in dB scale
        output_path: Path to save the spectrogram image (optional)
        show: Whether to display the plot interactively
    """
    plt.figure(figsize=(12, 6))
    
    # Display the spectrogram
    plt.pcolormesh(times, frequencies, spectrogram, shading='gouraud', cmap='viridis')
    
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram (Time-Frequency Domain)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.tight_layout()
    
    # Save if output path is provided
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Spectrogram saved to: {output_path}")
    
    # Show the plot
    if show:
        plt.show()
    else:
        plt.close()
