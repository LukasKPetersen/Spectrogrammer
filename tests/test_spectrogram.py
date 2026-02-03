"""
Unit tests for the Spectrogrammer application.
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
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
    
    def test_load_audio_with_valid_duration(self):
        """Test that load_audio successfully loads files within duration limit."""
        sample_rate = 44100
        duration = 3  # 3 seconds
        audio_data = np.random.randn(sample_rate * duration).astype(np.float32)
        
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Write audio data to file
            sf.write(tmp_path, audio_data, sample_rate)
            
            # Test load_audio function with a max_duration that allows this file
            loaded_audio, loaded_sr = load_audio(tmp_path, max_duration=10)
            
            # Verify the loaded audio matches what we wrote
            self.assertEqual(loaded_sr, sample_rate)
            self.assertAlmostEqual(len(loaded_audio) / loaded_sr, duration, places=1)
            self.assertGreater(len(loaded_audio), 0)
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_load_audio_exceeds_max_duration(self):
        """Test that load_audio raises ValueError when file exceeds max_duration."""
        sample_rate = 44100
        duration = 5  # 5 seconds
        audio_data = np.random.randn(sample_rate * duration).astype(np.float32)
        
        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Write audio data to file
            sf.write(tmp_path, audio_data, sample_rate)
            
            # Test that load_audio raises RuntimeError when max_duration is exceeded
            # (ValueError is caught and re-raised as RuntimeError in load_audio)
            with self.assertRaises(RuntimeError) as context:
                load_audio(tmp_path, max_duration=3)
            
            # Verify error message contains key information about duration violation
            error_msg = str(context.exception)
            self.assertIn("duration", error_msg.lower())
            self.assertIn("exceeds maximum", error_msg.lower())
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


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
        
        # Convert to mono by averaging
        if len(stereo_audio.shape) > 1:
            mono_audio = np.mean(stereo_audio, axis=1)
        else:
            mono_audio = stereo_audio
        
        # Check that result is 1D
        self.assertEqual(len(mono_audio.shape), 1)
        self.assertEqual(len(mono_audio), sample_rate)


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
