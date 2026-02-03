"""
Main application for generating spectrograms from audio files.
"""
import argparse
import sys
from pathlib import Path

from input_handler import load_audio
from spectrogram_processor import generate_spectrogram, plot_spectrogram


def main():
    """Main entry point for the spectrogram generator."""
    parser = argparse.ArgumentParser(
        description='Generate spectrogram from an audio file (up to 6 minutes)'
    )
    parser.add_argument(
        'audio_file',
        type=str,
        help='Path to the input audio file'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Path to save the spectrogram image (optional)'
    )
    parser.add_argument(
        '--no-show',
        action='store_true',
        help='Do not display the spectrogram interactively'
    )
    
    args = parser.parse_args()
    
    try:
        # Load audio file
        print("Loading audio file...")
        audio, sample_rate = load_audio(args.audio_file, max_duration=360)
        
        # Generate spectrogram
        print("Generating spectrogram...")
        frequencies, times, spectrogram = generate_spectrogram(audio, sample_rate)
        
        # Set default output path if not provided
        output_path = args.output
        if output_path is None and args.no_show:
            # If not showing and no output specified, create default output name
            input_path = Path(args.audio_file)
            output_path = str(input_path.with_suffix('.png'))
        
        # Plot spectrogram
        print("Plotting spectrogram...")
        plot_spectrogram(
            frequencies,
            times,
            spectrogram,
            output_path=output_path,
            show=not args.no_show
        )
        
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
