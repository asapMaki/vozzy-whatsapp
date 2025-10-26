#!/usr/bin/env python3
"""
Media Workflow - Complete end-to-end media processing

Combines media processing and chat integration in a single workflow.
"""

import argparse
import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path


def run_command(cmd: list, description: str) -> tuple:
    """
    Run a command and return (success, output).

    Args:
        cmd: Command to run as list
        description: Human-readable description

    Returns:
        Tuple of (success: bool, output: str)
    """
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(e.stdout)
        print(e.stderr, file=sys.stderr)
        return False, e.stdout


def main():
    parser = argparse.ArgumentParser(
        description='Complete media processing workflow (process + integrate)',
        epilog='Example: python run_workflow.py (uses today) or python run_workflow.py --scan-date 24.10'
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--scan-date',
        type=str,
        metavar='DD.MM',
        help='Process all folders for a specific date (e.g., "24.10")'
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

    parser.add_argument(
        '--output-json',
        type=str,
        help='Save workflow results to JSON file'
    )

    args = parser.parse_args()

    # Determine repository root
    script_dir = Path(__file__).parent.parent.parent.parent.parent
    import os
    os.chdir(script_dir)

    workflow_results = {
        'started_at': datetime.now().isoformat(),
        'steps': [],
        'success': True
    }

    print(f"\n{'#'*60}")
    print(f"# GASTROHEM MEDIA WORKFLOW")
    print(f"{'#'*60}")

    # Build commands
    media_processor_cmd = [
        'python',
        '.claude/skills/gastrohem-media-processor/scripts/process_media.py'
    ]

    integrator_cmd = [
        'python',
        '.claude/skills/chat-integrator/scripts/integrate_media.py'
    ]

    # Add common arguments
    if args.scan_date:
        media_processor_cmd.extend(['--scan-date', args.scan_date])
        integrator_cmd.extend(['--scan-date', args.scan_date])
    elif args.folder:
        media_processor_cmd.extend(['--folder', args.folder])
        integrator_cmd.extend(['--folder', args.folder])

    if args.base_path != 'gastrohem whatsapp':
        media_processor_cmd.extend(['--base-path', args.base_path])
        integrator_cmd.extend(['--base-path', args.base_path])

    if args.dry_run:
        integrator_cmd.append('--dry-run')

    if args.no_backup:
        integrator_cmd.append('--no-backup')

    # Step 1: Process media (audio + images)
    success, output = run_command(
        media_processor_cmd,
        "STEP 1: Processing Media (Audio Transcription + Image OCR)"
    )
    workflow_results['steps'].append({
        'step': 1,
        'name': 'media_processing',
        'success': success,
        'output': output
    })

    if not success:
        workflow_results['success'] = False
        print(f"\n❌ Workflow failed at Step 1: Media Processing")
        if args.output_json:
            with open(args.output_json, 'w', encoding='utf-8') as f:
                json.dump(workflow_results, f, ensure_ascii=False, indent=2)
        return 1

    # Step 2: Integrate into chat.md
    success, output = run_command(
        integrator_cmd,
        "STEP 2: Integrating Media into chat.md"
    )
    workflow_results['steps'].append({
        'step': 2,
        'name': 'chat_integration',
        'success': success,
        'output': output
    })

    if not success:
        workflow_results['success'] = False
        print(f"\n❌ Workflow failed at Step 2: Chat Integration")
        if args.output_json:
            with open(args.output_json, 'w', encoding='utf-8') as f:
                json.dump(workflow_results, f, ensure_ascii=False, indent=2)
        return 1

    # Final summary
    workflow_results['completed_at'] = datetime.now().isoformat()

    print(f"\n{'#'*60}")
    print(f"# ✅ WORKFLOW COMPLETED SUCCESSFULLY")
    print(f"{'#'*60}")

    if args.output_json:
        with open(args.output_json, 'w', encoding='utf-8') as f:
            json.dump(workflow_results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Workflow results saved to: {args.output_json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
