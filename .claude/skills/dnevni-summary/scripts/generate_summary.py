#!/usr/bin/env python3
"""
Daily Summary Generator - Creates summary.md in each daily folder

Generates summary for each department's daily folder separately.
"""

import argparse
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re


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


def parse_chat_message(line: str) -> Tuple[str, str, str]:
    """Parse a chat.md line into (timestamp, sender, message)."""
    pattern = r'\[(\d{1,2}\. \d{1,2}\. \d{4}\., \d{2}:\d{2}:\d{2})\]\s*(?:\[(?:AUDIO|IMAGE)\])?\s*([^:]+):\s*(.*)'
    match = re.match(pattern, line)

    if match:
        timestamp, sender, message = match.groups()
        return timestamp.strip(), sender.strip(), message.strip()

    return None, None, None


def read_chat_file(chat_file: Path) -> List[Tuple[str, str, str]]:
    """Read chat.md file and parse all messages."""
    if not chat_file.exists():
        return []

    messages = []
    with open(chat_file, 'r', encoding='utf-8') as f:
        current_message = None

        for line in f:
            timestamp, sender, message = parse_chat_message(line)

            if timestamp and sender:
                # New message
                if current_message:
                    messages.append(current_message)
                current_message = (timestamp, sender, message)
            elif current_message:
                # Continuation of previous message
                ts, snd, msg = current_message
                current_message = (ts, snd, msg + "\n" + line.rstrip())

        # Add last message
        if current_message:
            messages.append(current_message)

    return messages


def aggregate_messages_by_person(messages: List[Tuple[str, str, str]]) -> Dict[str, List[str]]:
    """Aggregate messages by person."""
    by_person = defaultdict(list)

    for timestamp, sender, message in messages:
        by_person[sender].append(f"[{timestamp}] {message}")

    return dict(by_person)


def parse_date(date_str: str) -> Tuple[int, int]:
    """Parse DD.MM format to (day, month)."""
    parts = date_str.split('.')
    return int(parts[0]), int(parts[1])


def find_previous_weekly_summary(daily_folder: Path) -> Optional[Path]:
    """
    Find previous week's summary for the same department.

    Args:
        daily_folder: Path to current daily folder (e.g., gastrohem whatsapp/dept/20.10 - 27.10/24.10)

    Returns:
        Path to previous sedmicni-summary.md or None
    """
    weekly_folder = daily_folder.parent  # 20.10 - 27.10
    dept_folder = weekly_folder.parent    # dept

    current_day, current_month = parse_date(daily_folder.name)

    # Find all weekly folders in this department
    weekly_folders = []
    for folder in dept_folder.iterdir():
        if folder.is_dir() and re.match(r'^\d{2}\.\d{2} - \d{2}\.\d{2}$', folder.name):
            # Parse start date of week
            start_date = folder.name.split(' - ')[0]
            start_day, start_month = parse_date(start_date)

            # Only consider weeks before current date
            if (start_month < current_month) or (start_month == current_month and start_day < current_day):
                weekly_folders.append((folder, start_month, start_day))

    if not weekly_folders:
        return None

    # Sort by date descending and get most recent
    weekly_folders.sort(key=lambda x: (x[1], x[2]), reverse=True)
    most_recent_weekly = weekly_folders[0][0]

    sedmicni_summary = most_recent_weekly / 'sedmicni-summary.md'
    if sedmicni_summary.exists():
        return sedmicni_summary

    return None


def parse_weekly_summary_tasks(weekly_summary_file: Path) -> Dict[str, List[str]]:
    """
    Parse tasks from weekly summary's "Plan za narednu sedmicu" sections.

    Returns: Dict of {person_name: [task1, task2, ...]}
    """
    with open(weekly_summary_file, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks_by_person = {}

    # Split by person sections (## **Name**)
    person_sections = re.split(r'\n## \*\*([^*]+)\*\*', content)

    # First element is header, then alternating name/content
    for i in range(1, len(person_sections), 2):
        person_name = person_sections[i].strip()
        person_content = person_sections[i + 1] if i + 1 < len(person_sections) else ""

        # Find "Plan za narednu sedmicu" section
        plan_match = re.search(
            r'### Plan za narednu sedmicu:(.+?)(?=###|\n## |\Z)',
            person_content,
            re.DOTALL
        )

        if plan_match:
            plan_text = plan_match.group(1)
            tasks = []

            for line in plan_text.strip().split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    task = line.lstrip('- ').strip()
                    if task and not task.startswith('Nastaviti sa tekućim'):
                        tasks.append(task)

            if tasks:
                tasks_by_person[person_name] = tasks

    return tasks_by_person


def find_previous_daily_summaries(daily_folder: Path) -> List[Path]:
    """
    Find all previous daily summaries in the same week.

    Args:
        daily_folder: Path to current daily folder

    Returns:
        List of paths to previous summary.md files (sorted chronologically)
    """
    weekly_folder = daily_folder.parent
    current_day, current_month = parse_date(daily_folder.name)

    previous_summaries = []

    # Find all daily folders in this week
    for folder in weekly_folder.iterdir():
        if folder.is_dir() and re.match(r'^\d{2}\.\d{2}$', folder.name):
            day, month = parse_date(folder.name)

            # Only consider days before current date
            if (month < current_month) or (month == current_month and day < current_day):
                summary_file = folder / 'summary.md'
                if summary_file.exists():
                    previous_summaries.append((summary_file, month, day))

    # Sort chronologically
    previous_summaries.sort(key=lambda x: (x[1], x[2]))

    return [s[0] for s in previous_summaries]


def parse_daily_summary_tasks(summary_file: Path) -> Dict[str, List[str]]:
    """
    Extract potential tasks from daily summary activities.

    Looks for patterns like:
    - "treba", "trebao", "potrebno"
    - "sutra", "sljedeći", "planirati"
    - Questions that imply tasks

    Returns: Dict of {person_name: [task1, task2, ...]}
    """
    with open(summary_file, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks_by_person = {}

    # Split by person sections
    person_sections = re.split(r'\n## \*\*([^*]+)\*\*', content)

    for i in range(1, len(person_sections), 2):
        person_name = person_sections[i].strip()
        person_content = person_sections[i + 1] if i + 1 < len(person_sections) else ""

        # Find aktivnosti
        aktivnosti_match = re.search(
            r'\*\*Aktivnosti:\*\*(.+?)(?=\n## |\*\*Broj poruka|\Z)',
            person_content,
            re.DOTALL
        )

        if not aktivnosti_match:
            continue

        aktivnosti_text = aktivnosti_match.group(1)
        tasks = []

        # Task indicators
        task_keywords = [
            'treba', 'trebao', 'trebala', 'potrebno',
            'sutra', 'sljedeć', 'planirati', 'organizovat',
            'moramo', 'moram', 'mora', 'ću', 'cu'
        ]

        for line in aktivnosti_text.strip().split('\n'):
            line = line.strip()
            if not line.startswith('-'):
                continue

            # Remove timestamp and dash
            clean_line = re.sub(r'- \[.*?\]\s*', '', line).strip()

            if not clean_line:
                continue

            # Check if line contains task keywords
            line_lower = clean_line.lower()
            if any(keyword in line_lower for keyword in task_keywords):
                # Limit length
                if len(clean_line) > 100:
                    clean_line = clean_line[:100] + "..."
                tasks.append(clean_line)

        if tasks:
            tasks_by_person[person_name] = tasks

    return tasks_by_person


def generate_summary_for_folder(folder: Path) -> bool:
    """
    Generate summary.md for a specific folder.

    Args:
        folder: Path to daily folder

    Returns:
        True if summary was generated
    """
    chat_file = folder / 'chat.md'
    summary_file = folder / 'summary.md'

    dept_name = folder.parent.parent.name
    date = folder.name

    print(f"\n📁 {dept_name}/{date}")

    # Read chat.md
    messages = read_chat_file(chat_file)

    if not messages:
        print(f"   ⏭️  No messages found, skipping")
        return False

    print(f"   📊 {len(messages)} messages")

    # Aggregate by person
    by_person = aggregate_messages_by_person(messages)

    # Check for previous week's tasks
    weekly_tasks = {}
    prev_weekly_summary = find_previous_weekly_summary(folder)
    if prev_weekly_summary:
        weekly_tasks = parse_weekly_summary_tasks(prev_weekly_summary)
        if weekly_tasks:
            print(f"   📝 Found tasks from previous week's summary")

    # Check for previous daily summaries in this week
    daily_tasks = {}
    prev_daily_summaries = find_previous_daily_summaries(folder)
    if prev_daily_summaries:
        print(f"   📝 Found {len(prev_daily_summaries)} previous daily summaries")
        for prev_summary_file in prev_daily_summaries:
            day_tasks = parse_daily_summary_tasks(prev_summary_file)
            # Merge tasks
            for person, tasks in day_tasks.items():
                if person not in daily_tasks:
                    daily_tasks[person] = []
                daily_tasks[person].extend(tasks)

    # Generate summary
    summary_lines = []
    summary_lines.append(f"# Summary - {dept_name.title()} ({date})\n\n")
    summary_lines.append(f"**Ukupno poruka:** {len(messages)}  \n")
    summary_lines.append(f"**Aktivnih osoba:** {len(by_person)}\n\n")

    # Add tasks section if any tasks found
    if weekly_tasks or daily_tasks:
        summary_lines.append("## 📋 Taskovi iz prethodnih perioda\n\n")

        if weekly_tasks:
            summary_lines.append("### Iz prošle sedmice:\n")
            for person in sorted(weekly_tasks.keys()):
                summary_lines.append(f"**{person}:**\n")
                for task in weekly_tasks[person]:
                    summary_lines.append(f"- {task}\n")
                summary_lines.append("\n")

        if daily_tasks:
            summary_lines.append("### Iz prethodnih dana ove sedmice:\n")
            for person in sorted(daily_tasks.keys()):
                summary_lines.append(f"**{person}:**\n")
                for task in daily_tasks[person][:5]:  # Limit to 5 most recent
                    summary_lines.append(f"- {task}\n")
                summary_lines.append("\n")

    summary_lines.append("---\n\n")

    # Messages by person
    for person in sorted(by_person.keys()):
        messages_list = by_person[person]
        summary_lines.append(f"## **{person}**\n")
        summary_lines.append(f"**Broj poruka:** {len(messages_list)}\n")

        # Show condensed version - just first line of each message
        summary_lines.append("**Aktivnosti:**\n")
        for msg in messages_list[:10]:  # Limit to first 10
            # Extract just first line
            first_line = msg.split('\n')[0]
            if len(first_line) > 120:
                first_line = first_line[:120] + "..."
            summary_lines.append(f"- {first_line}\n")

        if len(messages_list) > 10:
            summary_lines.append(f"- ... i još {len(messages_list) - 10} poruka\n")

        summary_lines.append("\n")

    summary_lines.append("---\n")
    summary_lines.append(f"\n*Generisano: {datetime.now().strftime('%d.%m.%Y %H:%M')}*\n")

    summary_text = ''.join(summary_lines)

    # Write summary.md
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_text)

    print(f"   ✅ Summary created: {len(by_person)} people")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Generate summary.md in each daily folder',
        epilog='Example: python generate_summary.py --date 24.10'
    )

    parser.add_argument(
        '--date',
        type=str,
        metavar='DD.MM',
        help='Date to summarize (e.g., "24.10"). Default: today'
    )

    parser.add_argument(
        '--base-path',
        type=str,
        default='gastrohem whatsapp',
        help='Base path for scanning (default: "gastrohem whatsapp")'
    )

    parser.add_argument(
        '--folder',
        type=str,
        help='Process specific folder only'
    )

    args = parser.parse_args()

    # Determine repository root
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    import os
    os.chdir(script_dir)

    print(f"\n{'='*60}")
    print(f"📋 Generating Per-Folder Summaries")
    print(f"{'='*60}")

    if args.folder:
        # Process single folder
        folder = Path(args.folder)
        if generate_summary_for_folder(folder):
            print(f"\n✅ Summary generated for {folder}")
        else:
            print(f"\n❌ No summary generated for {folder}")
        return

    # Determine date
    if args.date:
        target_date = args.date
    else:
        target_date = datetime.now().strftime('%d.%m')
        print(f"📅 No date specified, using today: {target_date}")

    base_path = Path(args.base_path)

    # Find all folders for date
    folders = find_daily_folders_for_date(base_path, target_date)

    if not folders:
        print(f"\n❌ No folders found for date: {target_date}")
        return

    print(f"\n🔍 Found {len(folders)} folder(s) for {target_date}")

    # Generate summary for each folder
    generated = 0
    for folder in folders:
        if generate_summary_for_folder(folder):
            generated += 1

    print(f"\n{'='*60}")
    print(f"✅ Generated {generated} summaries out of {len(folders)} folders")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
