#!/usr/bin/env python3
"""
Media Processor - Master Script for Gastrohem WhatsApp Documentation

Combines audio transcription and image OCR processing.
Uses separate scripts for audio (process_audio.py) and images (process_images.py).
"""

import argparse
import json
import sys
from pathlib import Path

# Import from separate processing scripts
from process_audio import process_folder as process_audio_folder, find_audio_files
from process_images import get_images_needing_ocr, find_image_files


def find_daily_folders_for_date(base_path: Path, target_date: str) -> list[Path]:
    """
    Find all daily folders matching the target date across all departments.

    Args:
        base_path: Root path (e.g., 'gastrohem whatsapp')
        target_date: Date in format 'DD.MM' (e.g., '26.10')

    Returns:
        List of Path objects for matching daily folders
    """
    matching_folders = []

    # Departments to scan
    departments = [
        'administracija', 'finansije', 'prodaja',
        'servis', 'svaštara', 'sastanci menadžmenta', 'adis-chat'
    ]

    for dept in departments:
        dept_path = base_path / dept
        if not dept_path.exists():
            continue

        # Scan all weekly folders
        for weekly_folder in dept_path.iterdir():
            if not weekly_folder.is_dir():
                continue

            # Check for daily folder matching the target date
            daily_folder = weekly_folder / target_date
            if daily_folder.exists() and daily_folder.is_dir():
                matching_folders.append(daily_folder)

    return matching_folders


def process_folder(folder_path: Path, skip_existing: bool = True) -> dict:
    """
    Process all media files (audio and images) in a folder.

    Args:
        folder_path: Path to the folder
        skip_existing: Skip files that already have JSON

    Returns:
        Dictionary with processing results
    """
    folder_path = Path(folder_path).resolve()

    if not folder_path.exists():
        print(f"❌ Error: Folder does not exist: {folder_path}")
        return None

    print(f"\n{'='*60}")
    print(f"📂 Processing media in: {folder_path}")
    print(f"{'='*60}")

    # Process audio files
    print(f"\n🎵 AUDIO PROCESSING")
    print(f"-" * 60)
    audio_results = process_audio_folder(folder_path, skip_existing)

    # Get images needing OCR
    print(f"\n🖼️  IMAGE PROCESSING")
    print(f"-" * 60)
    images_needing_ocr = get_images_needing_ocr(folder_path, skip_existing)
    all_images = find_image_files(folder_path)

    print(f"\n📊 Image Summary:")
    print(f"  📷 Total images: {len(all_images)}")
    print(f"  🖼️  Needs OCR: {len(images_needing_ocr)}")
    print(f"  ✅ Already processed: {len(all_images) - len(images_needing_ocr)}")

    if images_needing_ocr:
        print(f"\n📋 Images needing OCR:")
        for img in images_needing_ocr:
            print(f"  - {img.name}")

    # Combined results
    results = {
        'folder': str(folder_path),
        'audio': audio_results if audio_results else {},
        'images': {
            'total': len(all_images),
            'needs_ocr': [str(img) for img in images_needing_ocr],
            'already_processed': len(all_images) - len(images_needing_ocr)
        }
    }

    return results


def process_all_folders_for_date(base_path: Path, target_date: str, skip_existing: bool = True) -> dict:
    """
    Process all daily folders matching the target date across all departments.

    Args:
        base_path: Root path
        target_date: Date in format 'DD.MM'
        skip_existing: Skip files with existing JSON

    Returns:
        Dictionary with aggregated results from all folders
    """
    matching_folders = find_daily_folders_for_date(base_path, target_date)

    if not matching_folders:
        print(f"❌ No folders found for date: {target_date}")
        return {
            'total_folders': 0,
            'total_audio_transcribed': 0,
            'total_images_needing_ocr': 0,
            'folders_processed': []
        }

    print(f"\n🔍 Found {len(matching_folders)} folder(s) for date {target_date}:")
    for folder in matching_folders:
        print(f"  📁 {folder.relative_to(base_path)}")

    all_results = {
        'date': target_date,
        'total_folders': len(matching_folders),
        'total_audio_transcribed': 0,
        'total_images_needing_ocr': 0,
        'folders_processed': [],
        'all_images_needing_ocr': []
    }

    # Process each folder
    for folder in matching_folders:
        result = process_folder(folder, skip_existing)
        if result:
            # Count audio transcribed
            if result.get('audio'):
                all_results['total_audio_transcribed'] += len(result['audio'].get('transcribed', []))

            # Count images needing OCR
            all_results['total_images_needing_ocr'] += len(result['images'].get('needs_ocr', []))
            all_results['all_images_needing_ocr'].extend(result['images'].get('needs_ocr', []))

            all_results['folders_processed'].append(result)

    print(f"\n{'='*60}")
    print(f"🎯 FINAL SUMMARY FOR {target_date}")
    print(f"{'='*60}")
    print(f"  📂 Folders processed: {all_results['total_folders']}")
    print(f"  🎵 Total audio transcribed: {all_results['total_audio_transcribed']}")
    print(f"  🖼️  Total images needing OCR: {all_results['total_images_needing_ocr']}")

    if all_results['all_images_needing_ocr']:
        print(f"\n📋 All images needing OCR ({len(all_results['all_images_needing_ocr'])}):")
        for img in all_results['all_images_needing_ocr']:
            print(f"  - {img}")

    return all_results


def main():
    parser = argparse.ArgumentParser(
        description='Process audio and image files for Gastrohem documentation',
        epilog='Example: python process_media.py (uses today\'s date) or python process_media.py --scan-date 26.10'
    )

    # Optional: either scan a date or process a specific folder
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--scan-date',
        type=str,
        metavar='DD.MM',
        help='Scan and process all folders for a specific date (e.g., "26.10"). If not specified, uses today\'s date.'
    )
    group.add_argument(
        '--folder',
        type=str,
        help='Process a specific folder (e.g., "gastrohem whatsapp/administracija/20.10 - 27.10/24.10")'
    )

    parser.add_argument(
        '--base-path',
        type=str,
        default='gastrohem whatsapp',
        help='Base path for scanning (default: "gastrohem whatsapp")'
    )

    parser.add_argument(
        '--no-skip-existing',
        action='store_true',
        help='Re-process files that already have JSON files'
    )

    parser.add_argument(
        '--output-json',
        type=str,
        help='Save results to JSON file'
    )

    args = parser.parse_args()

    # Determine the repository root
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    import os
    os.chdir(script_dir)

    skip_existing = not args.no_skip_existing

    if args.folder:
        # Process a specific folder
        results = process_folder(Path(args.folder), skip_existing)
    else:
        # Scan all folders for a date (use today's date if not specified)
        if args.scan_date:
            target_date = args.scan_date
        else:
            # Use today's date in DD.MM format
            from datetime import datetime
            target_date = datetime.now().strftime('%d.%m')
            print(f"📅 No date specified, using today's date: {target_date}")

        base_path = Path(args.base_path)
        results = process_all_folders_for_date(base_path, target_date, skip_existing)

    # Optionally save results to JSON
    if args.output_json and results:
        with open(args.output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Results saved to: {args.output_json}")


if __name__ == "__main__":
    main()
