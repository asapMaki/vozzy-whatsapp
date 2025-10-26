#!/usr/bin/env python3
"""
Sedmični Summary Generator

Agregira sve dnevne summary-e iz sedmičnog foldera u jedan sedmični summary.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import re
import sys
import argparse


def get_repo_root() -> Path:
    """Get repository root (5 levels up from this script)."""
    return Path(__file__).parent.parent.parent.parent.parent


def find_weekly_folders() -> List[Tuple[Path, str]]:
    """
    Find all weekly folders in gastrohem whatsapp.
    Returns: List of (folder_path, department_name) tuples
    """
    repo_root = get_repo_root()
    whatsapp_dir = repo_root / "gastrohem whatsapp"

    weekly_folders = []

    # Pattern for weekly folders: DD.MM - DD.MM
    week_pattern = re.compile(r'^\d{2}\.\d{2} - \d{2}\.\d{2}$')

    # Iterate through department folders
    for dept_dir in whatsapp_dir.iterdir():
        if not dept_dir.is_dir():
            continue

        # Find weekly folders in this department
        for item in dept_dir.iterdir():
            if item.is_dir() and week_pattern.match(item.name):
                weekly_folders.append((item, dept_dir.name))

    return weekly_folders


def find_daily_summaries(weekly_folder: Path) -> List[Path]:
    """
    Find all daily summary.md files in a weekly folder.
    Returns: List of summary.md file paths
    """
    summaries = []

    # Pattern for daily folders: DD.MM
    daily_pattern = re.compile(r'^\d{2}\.\d{2}$')

    for item in weekly_folder.iterdir():
        if item.is_dir() and daily_pattern.match(item.name):
            summary_file = item / 'summary.md'
            if summary_file.exists():
                summaries.append(summary_file)

    # Sort by date
    summaries.sort(key=lambda p: p.parent.name)

    return summaries


def parse_daily_summary(summary_file: Path) -> Dict[str, Dict[str, List[str]]]:
    """
    Parse a daily summary.md file.

    Supports three formats:
    1. Person-based format with "**Aktivnosti:**" section
    2. Person-based legacy format with "### Što je uradio:" and "### Što bi trebao da uradi:"
    3. Topic-based format (Finansije, Servis) - extracts all bullet points as activities

    Returns: Dict of {person_name: {'uradio': [...], 'trebao': [...]}}
    """
    with open(summary_file, 'r', encoding='utf-8') as f:
        content = f.read()

    people_data = {}

    # Split by person sections (## **Name**)
    person_sections = re.split(r'\n## \*\*([^*]+)\*\*', content)

    # Check if this is a person-based summary (has ## **Name** sections)
    if len(person_sections) > 1:
        # PERSON-BASED FORMAT
        # First element is header, then alternating name/content
        for i in range(1, len(person_sections), 2):
            person_name = person_sections[i].strip()
            person_content = person_sections[i + 1] if i + 1 < len(person_sections) else ""

            if person_name not in people_data:
                people_data[person_name] = {'uradio': [], 'trebao': []}

            # Try current format first: **Aktivnosti:**
            aktivnosti_match = re.search(
                r'\*\*Aktivnosti:\*\*(.+?)(?=\n## |\*\*Broj poruka|\Z)',
                person_content,
                re.DOTALL
            )

            if aktivnosti_match:
                # Current format
                aktivnosti_text = aktivnosti_match.group(1)
                aktivnosti_items = []

                for line in aktivnosti_text.strip().split('\n'):
                    line = line.strip()
                    if line.startswith('-'):
                        # Remove timestamp and get the activity text
                        # Format: - [DD. MM. YYYY., HH:MM:SS] text
                        clean_line = re.sub(r'- \[.*?\]\s*', '', line).strip()
                        if clean_line:  # Only add non-empty activities
                            aktivnosti_items.append(clean_line)

                people_data[person_name]['uradio'].extend(aktivnosti_items)

            else:
                # Try legacy format: "### Što je uradio:" and "### Što bi trebao da uradi:"
                # Extract "Što je uradio" section
                uradio_match = re.search(
                    r'### Što je uradio:(.+?)(?=###|$)',
                    person_content,
                    re.DOTALL
                )
                uradio_items = []
                if uradio_match:
                    uradio_text = uradio_match.group(1)
                    uradio_items = [
                        line.strip('- ').strip()
                        for line in uradio_text.strip().split('\n')
                        if line.strip().startswith('-')
                    ]

                # Extract "Što bi trebao da uradi" section
                trebao_match = re.search(
                    r'### Što bi trebao da uradi:(.+?)(?=###|$)',
                    person_content,
                    re.DOTALL
                )
                trebao_items = []
                if trebao_match:
                    trebao_text = trebao_match.group(1)
                    trebao_items = [
                        line.strip('- ').strip()
                        for line in trebao_text.strip().split('\n')
                        if line.strip().startswith('-')
                    ]

                people_data[person_name]['uradio'].extend(uradio_items)
                people_data[person_name]['trebao'].extend(trebao_items)

    else:
        # TOPIC-BASED FORMAT (e.g., Finansije, Servis)
        # Extract summary title to use as "person" name
        title_match = re.search(r'^# Summary - (.+?)(?:\n|$)', content, re.MULTILINE)
        topic_name = title_match.group(1).strip() if title_match else "Opšte"

        # Initialize data for this topic
        people_data[topic_name] = {'uradio': [], 'trebao': []}

        # Extract all bullet points as activities
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                # Remove checkbox markers if present
                clean_line = re.sub(r'- \[[ xX]\]\s*', '- ', line)
                clean_line = clean_line.strip('- ').strip()

                if clean_line and not clean_line.startswith('*'):  # Skip empty and italic lines
                    # Check if it's a completion item (checkbox)
                    if re.match(r'\[[ xX]\]', line.strip('- ')):
                        people_data[topic_name]['trebao'].append(clean_line)
                    else:
                        # Regular activity
                        people_data[topic_name]['uradio'].append(clean_line)

    return people_data


def is_completed_item(item: str) -> bool:
    """
    Check if an item is marked as completed.

    Checks for:
    - Checked checkboxes: [x] or [X]
    - Keywords: završeno, done, completed, gotovo
    """
    # Checked checkbox
    if re.search(r'\[x\]|\[X\]', item, re.IGNORECASE):
        return True

    # Completion keywords
    completion_keywords = ['završeno', 'done', 'completed', 'gotovo', 'urađeno']
    item_lower = item.lower()

    for keyword in completion_keywords:
        if keyword in item_lower:
            return True

    return False


def aggregate_weekly_data(daily_summaries: List[Path]) -> Dict[str, Dict[str, List[str]]]:
    """
    Aggregate data from all daily summaries.

    Returns: Dict of {person_name: {
        'aktivnosti': [...],
        'završeni': [...],
        'u_toku': [...]
    }}
    """
    weekly_data = {}

    for summary_file in daily_summaries:
        daily_data = parse_daily_summary(summary_file)
        day = summary_file.parent.name  # DD.MM

        for person, data in daily_data.items():
            if person not in weekly_data:
                weekly_data[person] = {
                    'aktivnosti': [],
                    'završeni': [],
                    'u_toku': []
                }

            # Add completed activities
            for item in data['uradio']:
                activity = f"[{day}] {item}"
                weekly_data[person]['aktivnosti'].append(activity)

                # Check if marked as completed
                if is_completed_item(item):
                    weekly_data[person]['završeni'].append(item)

            # Add planned items as ongoing
            for item in data['trebao']:
                if not is_completed_item(item):
                    weekly_data[person]['u_toku'].append(item)

    return weekly_data


def generate_next_week_plan(person_data: Dict[str, List[str]]) -> List[str]:
    """
    Generate plan for next week based on current week's data.

    Logic:
    - Include incomplete items from 'u_toku'
    - Suggest continuation of main activities
    """
    plan = []

    # Add incomplete items
    if person_data['u_toku']:
        plan.append("Nastaviti sa nedovršenim zadacima:")
        for item in person_data['u_toku'][:5]:  # Limit to 5
            # Remove checkbox if present
            clean_item = re.sub(r'\[[ xX]\]\s*', '', item)
            plan.append(f"  - {clean_item}")

    # Analyze activities for trends
    aktivnosti_text = ' '.join(person_data['aktivnosti']).lower()

    # Common activity patterns
    if 'sastanak' in aktivnosti_text or 'meeting' in aktivnosti_text:
        plan.append("- Planirati sljedeće sastanke")

    if 'dokument' in aktivnosti_text or 'dokumentacija' in aktivnosti_text:
        plan.append("- Nastaviti sa dokumentacijom")

    if 'nabavka' in aktivnosti_text or 'nabaviti' in aktivnosti_text:
        plan.append("- Finalizovati procese nabavke")

    if 'servis' in aktivnosti_text:
        plan.append("- Pratiti servisne intervencije")

    if 'prodaja' in aktivnosti_text or 'klijent' in aktivnosti_text:
        plan.append("- Follow-up sa klijentima")

    if not plan:
        plan.append("- Nastaviti sa tekućim aktivnostima")

    return plan


def generate_weekly_summary(weekly_folder: Path, dept_name: str) -> bool:
    """
    Generate sedmicni-summary.md for a weekly folder.

    Returns: True if successful, False otherwise
    """
    week_name = weekly_folder.name

    # Find all daily summaries
    daily_summaries = find_daily_summaries(weekly_folder)

    if not daily_summaries:
        print(f"⚠️  Nema dnevnih summary-a u {dept_name}/{week_name}")
        return False

    print(f"📊 Generiše se sedmični summary za {dept_name}/{week_name}")
    print(f"   Pronađeno {len(daily_summaries)} dnevnih summary-a")

    # Aggregate data
    weekly_data = aggregate_weekly_data(daily_summaries)

    if not weekly_data:
        print(f"⚠️  Nema podataka za agregaciju u {dept_name}/{week_name}")
        return False

    # Generate summary content
    summary_lines = []
    summary_lines.append(f"# Sedmični Summary - {dept_name.title()} ({week_name})\n\n")
    summary_lines.append(f"**Period:** {week_name}  \n")
    summary_lines.append(f"**Broj dana:** {len(daily_summaries)}  \n")
    summary_lines.append(f"**Aktivnih osoba:** {len(weekly_data)}\n\n")
    summary_lines.append("---\n\n")

    # Per person sections
    for person, data in sorted(weekly_data.items()):
        summary_lines.append(f"## **{person}**\n\n")

        # Activities during the week
        summary_lines.append("### Aktivnosti u sedmici:\n")
        if data['aktivnosti']:
            for activity in data['aktivnosti']:
                summary_lines.append(f"- {activity}\n")
        else:
            summary_lines.append("- *(Nema zabilježenih aktivnosti)*\n")
        summary_lines.append("\n")

        # Completed tasks
        summary_lines.append("### Završeni taskovi:\n")
        if data['završeni']:
            for item in data['završeni']:
                # Clean up the item
                clean_item = re.sub(r'\[x\]|\[X\]', '', item, flags=re.IGNORECASE).strip()
                summary_lines.append(f"- ✅ {clean_item}\n")
        else:
            summary_lines.append("- *(Nema eksplicitno označenih završenih taskova)*\n")
        summary_lines.append("\n")

        # Plan for next week
        summary_lines.append("### Plan za narednu sedmicu:\n")
        next_week_plan = generate_next_week_plan(data)
        for item in next_week_plan:
            summary_lines.append(f"{item}\n")
        summary_lines.append("\n")

    # Write to file
    output_file = weekly_folder / 'sedmicni-summary.md'
    summary_text = ''.join(summary_lines)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary_text)

    print(f"✅ Kreiran: {output_file.relative_to(get_repo_root())}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Generate weekly summaries from daily summaries'
    )
    parser.add_argument(
        '--week',
        type=str,
        help='Specific week to process (e.g., "20.10 - 27.10")'
    )
    parser.add_argument(
        '--dept',
        type=str,
        help='Specific department to process'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("SEDMIČNI SUMMARY GENERATOR")
    print("=" * 60)
    print()

    # Find all weekly folders
    weekly_folders = find_weekly_folders()

    if not weekly_folders:
        print("❌ Nema pronađenih sedmičnih foldera")
        return 1

    # Filter by arguments if provided
    if args.week:
        weekly_folders = [
            (folder, dept) for folder, dept in weekly_folders
            if folder.name == args.week
        ]

    if args.dept:
        weekly_folders = [
            (folder, dept) for folder, dept in weekly_folders
            if dept == args.dept
        ]

    if not weekly_folders:
        print("❌ Nema foldera koji odgovaraju filterima")
        return 1

    print(f"Pronađeno {len(weekly_folders)} sedmičnih foldera za procesiranje\n")

    # Process each weekly folder
    success_count = 0
    for folder, dept in weekly_folders:
        if generate_weekly_summary(folder, dept):
            success_count += 1
        print()

    print("=" * 60)
    print(f"✅ Uspješno generirano: {success_count}/{len(weekly_folders)}")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
