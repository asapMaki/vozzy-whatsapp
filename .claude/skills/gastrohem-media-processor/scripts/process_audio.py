#!/usr/bin/env python3
"""
Audio Processor for Gastrohem WhatsApp Documentation

Transcribes audio files using insanely-fast-whisper with parallel processing.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Supported audio extensions
AUDIO_EXTENSIONS = {'.mp3', '.ogg', '.m4a', '.wav', '.opus'}


def find_audio_files(folder_path: Path) -> list[Path]:
    """Find all audio files in the folder."""
    audio_files = []

    for file in folder_path.iterdir():
        if file.is_file() and file.suffix.lower() in AUDIO_EXTENSIONS:
            audio_files.append(file)

    return audio_files


def has_transcription(audio_file: Path) -> bool:
    """Check if audio file already has a transcription JSON."""
    json_file = audio_file.parent / f"{audio_file.name}.json"
    return json_file.exists()


def transcribe_audio(audio_file: Path) -> tuple[Path, str, bool]:
    """
    Transcribe audio file using insanely-fast-whisper.

    Returns:
        tuple: (audio_file_path, transcribed_text, success)
    """
    json_output = audio_file.parent / f"{audio_file.name}.json"

    # Construct the command
    cmd = [
        'insanely-fast-whisper',
        '--file-name', str(audio_file),
        '--device-id', 'mps',
        '--model-name', 'ylacombe/whisper-large-v3-turbo',
        '--batch-size', '4',
        '--transcript-path', str(json_output),
        '--language', 'bosnian'
    ]

    print(f"🎵 Transcribing: {audio_file.name}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Read the JSON output and extract full text
        with open(json_output, 'r', encoding='utf-8') as f:
            transcript_data = json.load(f)
            # Extract the full text property
            full_text = transcript_data.get('text', '')
            return (audio_file, full_text.strip(), True)

    except subprocess.CalledProcessError as e:
        print(f"❌ Error transcribing {audio_file.name}: {e}")
        return (audio_file, "", False)
    except json.JSONDecodeError as e:
        print(f"❌ Error reading transcription JSON for {audio_file.name}: {e}")
        return (audio_file, "", False)


def transcribe_audio_parallel(audio_files: list[Path], max_workers: int = 3) -> dict:
    """
    Transcribe multiple audio files in parallel.

    Args:
        audio_files: List of audio file paths
        max_workers: Maximum number of parallel transcription processes

    Returns:
        Dictionary with results
    """
    results = {
        'transcribed': [],
        'failed': [],
        'total': len(audio_files)
    }

    if not audio_files:
        return results

    print(f"\n🚀 Starting parallel transcription of {len(audio_files)} audio file(s)...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all transcription tasks
        future_to_file = {executor.submit(transcribe_audio, audio_file): audio_file
                          for audio_file in audio_files}

        # Collect results as they complete
        for future in as_completed(future_to_file):
            audio_file, text, success = future.result()
            if success:
                results['transcribed'].append({
                    'file': str(audio_file),
                    'filename': audio_file.name,
                    'text': text
                })
                print(f"✅ Completed: {audio_file.name}")
            else:
                results['failed'].append(str(audio_file))
                print(f"⚠️  Failed: {audio_file.name}")

    return results


def process_folder(folder_path: Path, skip_existing: bool = True) -> dict:
    """
    Process all audio files in a folder.

    Args:
        folder_path: Path to the folder containing audio files
        skip_existing: Skip files that already have transcriptions

    Returns:
        Dictionary with processing results
    """
    folder_path = Path(folder_path).resolve()

    if not folder_path.exists():
        print(f"❌ Error: Folder does not exist: {folder_path}")
        return None

    print(f"\n📂 Processing audio in: {folder_path}")

    # Find all audio files
    all_audio = find_audio_files(folder_path)

    if not all_audio:
        print("✅ No audio files found.")
        return {
            'folder': str(folder_path),
            'total_audio': 0,
            'transcribed': [],
            'failed': [],
            'skipped': []
        }

    # Filter out files that already have transcriptions
    audio_to_process = []
    skipped = []

    for audio_file in all_audio:
        if skip_existing and has_transcription(audio_file):
            skipped.append(str(audio_file))
        else:
            audio_to_process.append(audio_file)

    if skipped:
        print(f"⏭️  Skipping {len(skipped)} file(s) with existing transcriptions")

    if not audio_to_process:
        print("✅ All audio files already transcribed.")
        return {
            'folder': str(folder_path),
            'total_audio': len(all_audio),
            'transcribed': [],
            'failed': [],
            'skipped': skipped
        }

    print(f"📊 Found {len(audio_to_process)} audio file(s) to process.")

    # Process audio files in parallel
    results = transcribe_audio_parallel(audio_to_process)

    print(f"\n📈 Summary:")
    print(f"  ✅ Transcribed: {len(results['transcribed'])}")
    print(f"  ❌ Failed: {len(results['failed'])}")
    print(f"  ⏭️  Skipped: {len(skipped)}")

    return {
        'folder': str(folder_path),
        'total_audio': len(all_audio),
        'transcribed': results['transcribed'],
        'failed': results['failed'],
        'skipped': skipped
    }


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe audio files for Gastrohem documentation',
        epilog='Example: python process_audio.py "gastrohem whatsapp/adis-chat/27.10 - 03.11/27.10"'
    )

    parser.add_argument(
        'folder',
        type=str,
        help='Path to the folder containing audio files'
    )

    parser.add_argument(
        '--max-workers',
        type=int,
        default=3,
        help='Maximum number of parallel transcription processes (default: 3)'
    )

    parser.add_argument(
        '--no-skip-existing',
        action='store_true',
        help='Re-transcribe files that already have transcriptions'
    )

    parser.add_argument(
        '--output-json',
        type=str,
        help='Save results to JSON file'
    )

    args = parser.parse_args()

    # Process the folder
    results = process_folder(
        Path(args.folder),
        skip_existing=not args.no_skip_existing
    )

    # Save results to JSON if requested
    if args.output_json and results:
        with open(args.output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Results saved to: {args.output_json}")


if __name__ == "__main__":
    main()
