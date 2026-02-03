"""
Unit tests for the Spectrogrammer application.
"""
import unittest
import numpy as np
import tempfile
import os
from pathlib import Path
import sys
import soundfile as sf

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.spectrogram_processor import generate_spectrogram, plot_spectrogram
from src.input_handler import load_audio


class TestSpectrogramGeneration(unittest.TestCase):
    """Test spectrogram generation functionality."""
    
    def test_generate_spectrogram_returns_correct_types(self):
        """Test that generate_spectrogram returns numpy arrays."""
        # Create a simple sine wave audio signal
        sample_rate = 44100
        duration = 1  # 1 second
        frequency = 440  # A4 note
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * frequency * t).astype(np.float32)
        
        frequencies, times, spectrogram = generate_spectrogram(audio, sample_rate)
        
        # Check that all returns are numpy arrays
        self.assertIsInstance(frequencies, np.ndarray)
        self.assertIsInstance(times, np.ndarray)
        self.assertIsInstance(spectrogram, np.ndarray)
    
    def test_generate_spectrogram_output_shapes(self):
        """Test that spectrogram dimensions are consistent."""
        sample_rate = 44100
        duration = 2  # 2 seconds
        audio = np.random.randn(sample_rate * duration).astype(np.float32)
        
        frequencies, times, spectrogram = generate_spectrogram(audio, sample_rate)
        
        # Check that spectrogram shape matches frequency and time dimensions
        self.assertEqual(spectrogram.shape[0], len(frequencies))
        self.assertEqual(spectrogram.shape[1], len(times))
        self.assertGreater(len(frequencies), 0)
        self.assertGreater(len(times), 0)


class TestAudioDuration(unittest.TestCase):
    """Test audio duration validation."""
    
    def test_audio_duration_check(self):
        """Test that audio duration is properly calculated."""
        sample_rate = 44100
        duration = 3  # 3 seconds
        audio = np.random.randn(sample_rate * duration).astype(np.float32)
        
        # Calculate duration from audio array
        calculated_duration = len(audio) / sample_rate
        
        self.assertAlmostEqual(calculated_duration, duration, places=2)
        self.assertGreater(calculated_duration, 0)


class TestMonoConversion(unittest.TestCase):
    """Test stereo to mono conversion."""
    
    def test_stereo_to_mono_conversion(self):
        """Test that stereo audio is properly converted to mono."""
        # Create stereo audio (2 channels)
        sample_rate = 44100
        duration = 1
        left_channel = np.sin(2 * np.pi * 440 * np.linspace(0, duration, sample_rate))
        right_channel = np.sin(2 * np.pi * 880 * np.linspace(0, duration, sample_rate))
        stereo_audio = np.column_stack((left_channel, right_channel))
        
        # Create temporary stereo WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Write stereo audio to file
            sf.write(tmp_path, stereo_audio, sample_rate)
            
            # Use load_audio to load and convert to mono
            mono_audio, loaded_sample_rate = load_audio(tmp_path)
            
            # Check that result is 1D (mono)
            self.assertEqual(len(mono_audio.shape), 1)
            self.assertEqual(loaded_sample_rate, sample_rate)
            self.assertEqual(len(mono_audio), sample_rate)
            
            # Verify that the mono audio is approximately the average of left and right channels
            # Convert expected to match the dtype returned by load_audio
            expected_mono = np.mean(stereo_audio, axis=1).astype(mono_audio.dtype)
            np.testing.assert_allclose(mono_audio, expected_mono, rtol=1e-4, atol=1e-4)
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestPlotSpectrogram(unittest.TestCase):
    """Test spectrogram plotting functionality."""
    
    def test_plot_spectrogram_saves_file(self):
        """Test that plot_spectrogram can save to a file."""
        # Generate test data
        sample_rate = 44100
        duration = 1
        audio = np.sin(2 * np.pi * 440 * np.linspace(0, duration, sample_rate * duration)).astype(np.float32)
        
        frequencies, times, spectrogram = generate_spectrogram(audio, sample_rate)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Save spectrogram without showing
            plot_spectrogram(frequencies, times, spectrogram, output_path=tmp_path, show=False)
            
            # Check that file was created
            self.assertTrue(os.path.exists(tmp_path))
            self.assertGreater(os.path.getsize(tmp_path), 0)
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


if __name__ == '__main__':
    unittest.main()
