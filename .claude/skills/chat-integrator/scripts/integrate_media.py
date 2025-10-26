#!/usr/bin/env python3
"""
Chat Integrator - Merges processed media into chat.md files

Automatically integrates audio transcriptions (.json) and image summaries (.md)
into chat.md at chronologically correct positions.
"""

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Audio and image extensions
AUDIO_EXTENSIONS = {'.mp3', '.ogg', '.m4a', '.wav', '.opus'}
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}


def extract_timestamp_from_whatsapp_filename(filename: str) -> Optional[datetime]:
    """
    Extract timestamp from WhatsApp filename formats.

    Supports:
    1. "WhatsApp Audio/Image/Video 2025-10-24 at 16.36.50.mp3"
    2. "AUDIO/PHOTO/IMAGE/VIDEO/PTT-2025-10-26-15-00-32.mp3"

    Returns: datetime object or None if parsing fails
    """
    # Pattern 1: WhatsApp [Audio/Image/Video] YYYY-MM-DD at HH.MM.SS
    pattern1 = r'(\d{4})-(\d{2})-(\d{2}) at (\d{2})\.(\d{2})\.(\d{2})'
    match = re.search(pattern1, filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        return datetime(int(year), int(month), int(day),
                       int(hour), int(minute), int(second))

    # Pattern 2: [AUDIO/PHOTO/IMAGE/VIDEO/PTT]-YYYY-MM-DD-HH-MM-SS
    pattern2 = r'(?:AUDIO|PHOTO|IMAGE|VIDEO|PTT)-(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})'
    match = re.search(pattern2, filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        return datetime(int(year), int(month), int(day),
                       int(hour), int(minute), int(second))

    return None


def format_timestamp_for_chat(dt: datetime) -> str:
    """
    Format datetime to chat.md timestamp format.

    Format: [DD. MM. YYYY., HH:MM:SS]
    """
    return f"[{dt.day:02d}. {dt.month:02d}. {dt.year}., {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}]"


def parse_timestamp_from_chat_line(line: str) -> Optional[datetime]:
    """
    Parse timestamp from chat.md line.

    Format: [DD. MM. YYYY., HH:MM:SS] Name: message
    """
    pattern = r'\[(\d{1,2})\. (\d{1,2})\. (\d{4})\., (\d{2}):(\d{2}):(\d{2})\]'
    match = re.match(pattern, line)

    if match:
        day, month, year, hour, minute, second = match.groups()
        return datetime(int(year), int(month), int(day),
                       int(hour), int(minute), int(second))

    return None


def find_processed_media(folder_path: Path) -> Dict[str, List[Path]]:
    """
    Find all processed media files in folder.

    Returns:
        Dict with 'audio' and 'images' lists of Path objects
    """
    results = {
        'audio': [],
        'images': []
    }

    for file in folder_path.iterdir():
        if not file.is_file():
            continue

        # Audio JSON files
        if file.suffix == '.json':
            # Check if it's an audio transcription (has audio extension in stem)
            stem = file.stem  # e.g., "WhatsApp Audio 2025-10-24 at 16.36.50.mp3"
            if any(ext in stem for ext in ['.mp3', '.ogg', '.m4a', '.wav', '.opus']):
                results['audio'].append(file)

        # Image MD files (but not chat.md or summary.md)
        elif file.suffix == '.md' and file.name not in ['chat.md', 'summary.md']:
            # Check if it's an image summary (has image extension in stem)
            stem = file.stem
            if any(ext in stem for ext in ['.png', '.jpg', '.jpeg', '.webp', '.bmp']):
                results['images'].append(file)

    return results


def read_audio_transcription(json_file: Path) -> str:
    """Read transcription text from audio JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get('text', '').strip()


def read_image_summary(md_file: Path) -> Tuple[str, str]:
    """
    Read summary from image MD file.

    Returns:
        Tuple of (summary_text, sender_name)
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract sender from "**Poslao:** Name" line
    sender = "Unknown"
    for line in lines:
        if line.startswith('**Poslao:**'):
            sender = line.replace('**Poslao:**', '').strip()
            break

    # Skip header (title, sender, date, separator)
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip() == '---':
            content_start = i + 1
            break

    # Join remaining lines
    summary = ''.join(lines[content_start:]).strip()
    return summary, sender


def create_chat_entry(timestamp: datetime, media_type: str, content: str, sender: str = "Unknown") -> str:
    """
    Create a chat.md entry for media.

    Args:
        timestamp: datetime object
        media_type: 'AUDIO' or 'IMAGE'
        content: transcription or summary text
        sender: name of sender

    Returns:
        Formatted string for chat.md
    """
    ts_str = format_timestamp_for_chat(timestamp)

    if media_type == 'AUDIO':
        # Single line format for audio
        return f"{ts_str} [AUDIO] {sender}: {content}\n"
    else:
        # Multi-line format for images
        lines = [
            f"{ts_str} [IMAGE] {sender}:\n",
            "\n",
            content,
            "\n"
        ]
        return ''.join(lines)


def entry_hash(timestamp: datetime, content: str) -> str:
    """
    Create hash for entry to detect duplicates.

    Args:
        timestamp: datetime object
        content: entry content

    Returns:
        Hash string
    """
    # Use timestamp + first 100 chars of content for hash
    key = f"{timestamp.isoformat()}:{content[:100]}"
    return hashlib.md5(key.encode()).hexdigest()


def is_duplicate(new_timestamp: datetime, new_content: str, existing_entries: List[Tuple[datetime, str]]) -> bool:
    """
    Check if entry already exists in existing entries.

    Args:
        new_timestamp: Timestamp of new entry
        new_content: Content of new entry
        existing_entries: List of (timestamp, content) tuples

    Returns:
        True if duplicate found
    """
    new_hash = entry_hash(new_timestamp, new_content)

    for existing_ts, existing_content in existing_entries:
        existing_hash = entry_hash(existing_ts, existing_content)
        if new_hash == existing_hash:
            return True

    return False


def parse_chat_md(chat_file: Path) -> List[Tuple[datetime, str]]:
    """
    Parse chat.md file into list of (timestamp, content) tuples.

    Returns:
        List of (datetime, full_line_content) tuples
    """
    if not chat_file.exists():
        return []

    entries = []
    with open(chat_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_entry = []
    current_timestamp = None

    for line in lines:
        # Check if line starts with timestamp
        ts = parse_timestamp_from_chat_line(line)

        if ts:
            # Save previous entry
            if current_timestamp and current_entry:
                entries.append((current_timestamp, ''.join(current_entry)))

            # Start new entry
            current_timestamp = ts
            current_entry = [line]
        else:
            # Continuation of current entry
            if current_entry:
                current_entry.append(line)

    # Save last entry
    if current_timestamp and current_entry:
        entries.append((current_timestamp, ''.join(current_entry)))

    return entries


def integrate_media_into_folder(folder_path: Path, dry_run: bool = False, backup: bool = True) -> Dict:
    """
    Integrate all processed media in a folder into chat.md.

    Args:
        folder_path: Path to folder containing chat.md and media files
        dry_run: If True, preview changes without writing
        backup: If True, create backup before modifying

    Returns:
        Dict with integration results
    """
    folder_path = Path(folder_path).resolve()
    chat_file = folder_path / 'chat.md'

    print(f"\n{'='*60}")
    print(f"📂 Processing: {folder_path}")
    print(f"{'='*60}")

    # Find processed media
    media = find_processed_media(folder_path)
    total_media = len(media['audio']) + len(media['images'])

    if total_media == 0:
        print("✅ No processed media found to integrate.")
        return {'integrated': 0, 'skipped': 0}

    print(f"\n📊 Found media:")
    print(f"  🎵 Audio: {len(media['audio'])}")
    print(f"  🖼️  Images: {len(media['images'])}")

    # Parse existing chat.md
    existing_entries = parse_chat_md(chat_file)
    print(f"  💬 Existing chat entries: {len(existing_entries)}")

    # Create new entries from media
    new_entries = []
    skipped = 0

    # Process audio files
    for audio_file in media['audio']:
        timestamp = extract_timestamp_from_whatsapp_filename(audio_file.name)

        if not timestamp:
            print(f"⚠️  Warning: Could not extract timestamp from {audio_file.name}")
            skipped += 1
            continue

        transcription = read_audio_transcription(audio_file)
        if not transcription:
            print(f"⚠️  Warning: Empty transcription in {audio_file.name}")
            skipped += 1
            continue

        # Try to infer sender from context (default: Unknown)
        sender = "Unknown"
        entry = create_chat_entry(timestamp, 'AUDIO', transcription, sender)

        # Check for duplicates
        if is_duplicate(timestamp, entry, existing_entries):
            print(f"  ⏭️  Skipped (duplicate): {audio_file.name}")
            skipped += 1
            continue

        new_entries.append((timestamp, entry))
        print(f"  ✅ Audio: {audio_file.name}")

    # Process image files
    for image_file in media['images']:
        # Try WhatsApp format first
        timestamp = extract_timestamp_from_whatsapp_filename(image_file.name)

        # Fallback to file modification time
        if not timestamp:
            mtime = image_file.stat().st_mtime
            timestamp = datetime.fromtimestamp(mtime)
            print(f"  ℹ️  Using file mtime for {image_file.name}")

        summary, sender = read_image_summary(image_file)
        if not summary:
            print(f"⚠️  Warning: Empty summary in {image_file.name}")
            skipped += 1
            continue

        entry = create_chat_entry(timestamp, 'IMAGE', summary, sender)

        # Check for duplicates
        if is_duplicate(timestamp, entry, existing_entries):
            print(f"  ⏭️  Skipped (duplicate): {image_file.name}")
            skipped += 1
            continue

        new_entries.append((timestamp, entry))
        print(f"  ✅ Image: {image_file.name}")

    # Merge and sort all entries
    all_entries = existing_entries + new_entries
    all_entries.sort(key=lambda x: x[0])  # Sort by timestamp

    # Write to chat.md
    integrated = len(new_entries)

    if dry_run:
        print(f"\n🔍 DRY RUN - Would integrate {integrated} entries")
        print("\nPreview of new entries:")
        for ts, content in new_entries:
            print(content)
        return {'integrated': 0, 'skipped': skipped, 'dry_run': True}

    # Create backup
    if backup and chat_file.exists():
        backup_file = folder_path / 'chat.md.backup'
        shutil.copy2(chat_file, backup_file)
        print(f"\n💾 Backup created: {backup_file.name}")

    # Write merged content
    with open(chat_file, 'w', encoding='utf-8') as f:
        for ts, content in all_entries:
            f.write(content)

    print(f"\n✅ Integrated {integrated} media entries into chat.md")
    if skipped > 0:
        print(f"⚠️  Skipped {skipped} entries (errors)")

    return {'integrated': integrated, 'skipped': skipped}


def find_folders_for_date(base_path: Path, target_date: str) -> List[Path]:
    """
    Find all daily folders matching the target date across departments.

    Args:
        base_path: Root path (e.g., 'gastrohem whatsapp')
        target_date: Date in format 'DD.MM' (e.g., '26.10')

    Returns:
        List of Path objects for matching folders
    """
    matching_folders = []

    departments = [
        'administracija', 'finansije', 'prodaja',
        'servis', 'svaštara', 'sastanci menadžmenta', 'adis-chat'
    ]

    for dept in departments:
        dept_path = base_path / dept
        if not dept_path.exists():
            continue

        for weekly_folder in dept_path.iterdir():
            if not weekly_folder.is_dir():
                continue

            daily_folder = weekly_folder / target_date
            if daily_folder.exists() and daily_folder.is_dir():
                matching_folders.append(daily_folder)

    return matching_folders


def main():
    parser = argparse.ArgumentParser(
        description='Integrate processed media into chat.md files',
        epilog='Example: python integrate_media.py (uses today) or python integrate_media.py --scan-date 24.10'
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--scan-date',
        type=str,
        metavar='DD.MM',
        help='Scan and process all folders for a specific date (e.g., "24.10")'
    )
    group.add_argument(
        '--folder',
        type=str,
        help='Process a specific folder'
    )

    parser.add_argument(
        '--base-path',
        type=str,
        default='gastrohem whatsapp',
        help='Base path for scanning (default: "gastrohem whatsapp")'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without writing'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup before modifying'
    )

    args = parser.parse_args()

    # Determine repository root
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    import os
    os.chdir(script_dir)

    backup = not args.no_backup

    if args.folder:
        # Process specific folder
        result = integrate_media_into_folder(Path(args.folder), args.dry_run, backup)
        total_integrated = result['integrated']
        total_skipped = result['skipped']
    else:
        # Scan all folders for a date
        if args.scan_date:
            target_date = args.scan_date
        else:
            # Use today's date
            target_date = datetime.now().strftime('%d.%m')
            print(f"📅 No date specified, using today's date: {target_date}")

        base_path = Path(args.base_path)
        folders = find_folders_for_date(base_path, target_date)

        if not folders:
            print(f"❌ No folders found for date: {target_date}")
            return

        print(f"\n🔍 Found {len(folders)} folder(s) for date {target_date}:")
        for folder in folders:
            print(f"  📁 {folder.relative_to(base_path)}")

        total_integrated = 0
        total_skipped = 0

        for folder in folders:
            result = integrate_media_into_folder(folder, args.dry_run, backup)
            total_integrated += result['integrated']
            total_skipped += result['skipped']

        print(f"\n{'='*60}")
        print(f"🎯 FINAL SUMMARY FOR {target_date}")
        print(f"{'='*60}")
        print(f"  📂 Folders processed: {len(folders)}")
        print(f"  ✅ Total media integrated: {total_integrated}")
        if total_skipped > 0:
            print(f"  ⚠️  Total skipped: {total_skipped}")


if __name__ == "__main__":
    main()
