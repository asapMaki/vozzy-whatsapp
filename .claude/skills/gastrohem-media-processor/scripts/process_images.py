#!/usr/bin/env python3
"""
Image OCR Processor for Gastrohem WhatsApp Documentation

Helper functions for batch OCR processing of images using Claude's vision capabilities.
Creates JSON files with OCR results.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Supported image extensions
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}


def find_image_files(folder_path: Path) -> list[Path]:
    """Find all image files in the folder."""
    image_files = []

    for file in folder_path.iterdir():
        if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS:
            image_files.append(file)

    return image_files


def has_ocr_md(image_file: Path) -> bool:
    """Check if image file already has an OCR markdown file."""
    md_file = image_file.parent / f"{image_file.name}.md"
    return md_file.exists()


def save_ocr_md(image_file: Path, summary: str, sender: str = "Mahir Kadic"):
    """
    Save OCR summary to markdown file with same name as image.

    Args:
        image_file: Path to the image file
        summary: Natural language summary of what's in the image (focus on Gastrohem-relevant info)
        sender: Name of the person who sent the image (default: Mahir Kadic)
    """
    md_output = image_file.parent / f"{image_file.name}.md"

    # Create markdown content
    md_content = f"# {image_file.name}\n\n"
    md_content += f"**Poslao:** {sender}  \n"
    md_content += f"**Datum:** {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
    md_content += "---\n\n"
    md_content += summary

    with open(md_output, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"💾 Saved OCR summary: {md_output.name}")
    return md_output


def get_images_needing_ocr(folder_path: Path, skip_existing: bool = True) -> list[Path]:
    """
    Find images that don't have OCR JSON files yet.

    Args:
        folder_path: Path to the folder containing images
        skip_existing: Skip images that already have OCR JSON

    Returns:
        List of image paths that need OCR processing
    """
    folder_path = Path(folder_path).resolve()

    if not folder_path.exists():
        print(f"❌ Error: Folder does not exist: {folder_path}")
        return []

    all_images = find_image_files(folder_path)

    if not all_images:
        print("✅ No image files found.")
        return []

    if not skip_existing:
        return all_images

    needs_ocr = []
    for image_file in all_images:
        if not has_ocr_md(image_file):
            needs_ocr.append(image_file)

    return needs_ocr


def list_images_for_ocr(folder_path: Path, skip_existing: bool = True) -> dict:
    """
    List all images that need OCR processing.

    Args:
        folder_path: Path to the folder
        skip_existing: Skip images with existing OCR JSON

    Returns:
        Dictionary with image information
    """
    folder_path = Path(folder_path).resolve()

    print(f"\n📂 Scanning for images in: {folder_path}")

    all_images = find_image_files(folder_path)
    needs_ocr = get_images_needing_ocr(folder_path, skip_existing)

    results = {
        'folder': str(folder_path),
        'total_images': len(all_images),
        'needs_ocr': [str(img) for img in needs_ocr],
        'already_processed': len(all_images) - len(needs_ocr)
    }

    print(f"\n📈 Summary:")
    print(f"  📷 Total images: {len(all_images)}")
    print(f"  🖼️  Needs OCR: {len(needs_ocr)}")
    print(f"  ✅ Already processed: {len(all_images) - len(needs_ocr)}")

    if needs_ocr:
        print(f"\n📋 Images needing OCR:")
        for img in needs_ocr:
            print(f"  - {img.name}")

    return results


def batch_save_ocr(ocr_results: list[dict]) -> dict:
    """
    Batch save OCR summaries for multiple images as markdown files.

    Args:
        ocr_results: List of dictionaries with OCR data:
            [
                {
                    'image_path': '/path/to/image.png',
                    'summary': 'Natural language summary of image content',
                    'sender': 'Mahir Kadic'  # optional
                },
                ...
            ]

    Returns:
        Dictionary with save results
    """
    results = {
        'saved': [],
        'failed': []
    }

    print(f"\n💾 Saving OCR summaries for {len(ocr_results)} image(s)...")

    for ocr_data in ocr_results:
        try:
            image_path = Path(ocr_data['image_path'])
            summary = ocr_data.get('summary', '')
            sender = ocr_data.get('sender', 'Mahir Kadic')

            md_file = save_ocr_md(image_path, summary, sender)
            results['saved'].append(str(md_file))

        except Exception as e:
            print(f"❌ Error saving OCR for {ocr_data.get('image_path')}: {e}")
            results['failed'].append(ocr_data.get('image_path'))

    print(f"\n📊 Batch save summary:")
    print(f"  ✅ Saved: {len(results['saved'])}")
    print(f"  ❌ Failed: {len(results['failed'])}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Image OCR helper for Gastrohem documentation',
        epilog='Example: python process_images.py "gastrohem whatsapp/administracija/20.10 - 27.10/24.10"'
    )

    parser.add_argument(
        'folder',
        type=str,
        help='Path to the folder containing images'
    )

    parser.add_argument(
        '--no-skip-existing',
        action='store_true',
        help='List all images including those with existing OCR'
    )

    parser.add_argument(
        '--output-json',
        type=str,
        help='Save list of images to JSON file'
    )

    args = parser.parse_args()

    # List images needing OCR
    results = list_images_for_ocr(
        Path(args.folder),
        skip_existing=not args.no_skip_existing
    )

    # Save results to JSON if requested
    if args.output_json:
        with open(args.output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Results saved to: {args.output_json}")


if __name__ == "__main__":
    main()
