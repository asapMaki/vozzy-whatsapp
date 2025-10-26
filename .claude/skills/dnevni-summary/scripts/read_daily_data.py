#!/usr/bin/env python3
"""
Read Daily Data - Load chat and task data for Claude to analyze

This script ONLY reads and displays data. It does NOT generate summaries.
Claude will analyze this output and generate structured summaries.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import re
from typing import List, Tuple, Optional, Dict


def get_repo_root() -> Path:
    """Get repository root (5 levels up from this script)."""
    return Path(__file__).parent.parent.parent.parent.parent


def find_daily_folders_for_date(base_path: Path, target_date: str) -> List[Path]:
    """Find all daily folders matching the target date."""
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


def read_chat_file(chat_file: Path) -> str:
    """Read entire chat.md file."""
    if not chat_file.exists():
        return ""

    with open(chat_file, 'r', encoding='utf-8') as f:
        return f.read()


def parse_date(date_str: str) -> Tuple[int, int]:
    """Parse DD.MM format to (day, month)."""
    parts = date_str.split('.')
    return int(parts[0]), int(parts[1])


def find_previous_weekly_summary(daily_folder: Path) -> Optional[Path]:
    """Find previous week's summary for the same department."""
    weekly_folder = daily_folder.parent
    dept_folder = weekly_folder.parent

    current_day, current_month = parse_date(daily_folder.name)

    # Find all weekly folders in this department
    weekly_folders = []
    for folder in dept_folder.iterdir():
        if folder.is_dir() and re.match(r'^\d{2}\.\d{2} - \d{2}\.\d{2}$', folder.name):
            start_date = folder.name.split(' - ')[0]
            start_day, start_month = parse_date(start_date)

            if (start_month < current_month) or (start_month == current_month and start_day < current_day):
                weekly_folders.append((folder, start_month, start_day))

    if not weekly_folders:
        return None

    weekly_folders.sort(key=lambda x: (x[1], x[2]), reverse=True)
    most_recent_weekly = weekly_folders[0][0]

    sedmicni_summary = most_recent_weekly / 'sedmicni-summary.md'
    if sedmicni_summary.exists():
        return sedmicni_summary

    return None


def find_previous_daily_summaries(daily_folder: Path) -> List[Path]:
    """Find all previous daily summaries in the same week."""
    weekly_folder = daily_folder.parent
    current_day, current_month = parse_date(daily_folder.name)

    previous_summaries = []

    for folder in weekly_folder.iterdir():
        if folder.is_dir() and re.match(r'^\d{2}\.\d{2}$', folder.name):
            day, month = parse_date(folder.name)

            if (month < current_month) or (month == current_month and day < current_day):
                summary_file = folder / 'summary.md'
                if summary_file.exists():
                    previous_summaries.append((summary_file, month, day))

    previous_summaries.sort(key=lambda x: (x[1], x[2]))
    return [s[0] for s in previous_summaries]


def read_file_safe(file_path: Path) -> str:
    """Read file with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"[Error reading file: {e}]"


def display_folder_data(folder: Path):
    """Display all data for a folder in structured format."""
    dept_name = folder.parent.parent.name
    date = folder.name

    print(f"\n{'='*70}")
    print(f"FOLDER: {dept_name} / {date}")
    print(f"{'='*70}\n")

    # Read chat.md
    chat_file = folder / 'chat.md'
    print(f"📁 CHAT.MD CONTENT:")
    print(f"-"*70)

    if chat_file.exists():
        chat_content = read_file_safe(chat_file)
        if chat_content:
            print(chat_content)
        else:
            print("(prazan fajl)")
    else:
        print("(chat.md ne postoji)")

    print(f"\n{'-'*70}\n")

    # Check for previous weekly summary
    prev_weekly = find_previous_weekly_summary(folder)
    if prev_weekly:
        print(f"📅 TASKOVI IZ PROŠLE SEDMICE:")
        print(f"   Izvor: {prev_weekly}")
        print(f"-"*70)
        content = read_file_safe(prev_weekly)
        # Extract only "Plan za narednu sedmicu" sections
        plan_sections = re.findall(
            r'(## \*\*[^*]+\*\*.*?### Plan za narednu sedmicu:.*?)(?=\n## |\Z)',
            content,
            re.DOTALL
        )
        if plan_sections:
            for section in plan_sections:
                print(section.strip())
                print()
        else:
            print("(nema taskova)")
        print(f"{'-'*70}\n")

    # Check for previous daily summaries
    prev_dailies = find_previous_daily_summaries(folder)
    if prev_dailies:
        print(f"📆 PRETHODNI DNEVNI SUMMARIES U SEDMICI:")
        for prev_summary in prev_dailies:
            print(f"   - {prev_summary}")
        print(f"-"*70)
        print("(Claude može da ih pročita za dodatni kontekst ako je potrebno)")
        print(f"{'-'*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Read daily chat data and previous tasks for Claude analysis'
    )

    parser.add_argument(
        '--date',
        type=str,
        metavar='DD.MM',
        help='Date to read (e.g., "24.10"). Default: today'
    )

    parser.add_argument(
        '--folder',
        type=str,
        help='Process specific folder only (relative or absolute path)'
    )

    args = parser.parse_args()

    # Determine repository root and change to it
    script_dir = get_repo_root()
    import os
    os.chdir(script_dir)

    print(f"\n{'='*70}")
    print(f"📖 READING DAILY DATA FOR CLAUDE ANALYSIS")
    print(f"{'='*70}")

    if args.folder:
        # Process single folder
        folder = Path(args.folder)
        if not folder.exists():
            print(f"\n❌ Folder does not exist: {folder}")
            return 1

        display_folder_data(folder)
        return 0

    # Determine date
    if args.date:
        target_date = args.date
    else:
        target_date = datetime.now().strftime('%d.%m')
        print(f"\n📅 No date specified, using today: {target_date}")

    base_path = Path('gastrohem whatsapp')

    # Find all folders for date
    folders = find_daily_folders_for_date(base_path, target_date)

    if not folders:
        print(f"\n❌ No folders found for date: {target_date}")
        return 1

    print(f"\n🔍 Found {len(folders)} folder(s) for {target_date}\n")

    # Display data for each folder
    for folder in folders:
        display_folder_data(folder)

    print(f"\n{'='*70}")
    print(f"✅ Data loaded for {len(folders)} folder(s)")
    print(f"📝 Claude should now analyze this data and generate structured summaries")
    print(f"{'='*70}\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
