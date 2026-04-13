#!/usr/bin/env python3
"""
Example: Paragraph Extract and Apply Workflow

This script demonstrates the paragraph extract/apply workflow, which allows you to:
1. Extract paragraph marker locations from one USFM file
2. Apply those paragraph markers to another USFM file
3. Save the paragraph map to a file for later use

This is useful for:
- Transferring paragraph formatting between translations
- Backing up and restoring paragraph markers
- Analyzing paragraph structure across different versions

Usage:
    # Extract paragraph markers from a file
    python example_paragraphs.py extract input.usfm paragraphs.txt
    
    # Apply paragraph markers to a file
    python example_paragraphs.py apply input.usfm paragraphs.txt output.acc
    
    # Show paragraph locations
    python example_paragraphs.py show input.usfm
"""

import sys
from pathlib import Path

# Add parent directory to path to import usfmtools
sys.path.insert(0, str(Path(__file__).parent.parent))

from usfmtools.usfmparser import UsfmParser
from usfmtools.usfmwalker import (
    ParagraphExtractWalker,
    ParagraphApplyWalker,
    AccordanceWalker
)


def extract_paragraphs(input_file: str, output_file: str):
    """
    Extract paragraph marker locations from a USFM file.
    
    Args:
        input_file: Path to USFM file
        output_file: Path to save paragraph map
    """
    # Parse the USFM file
    parser = UsfmParser()
    document = parser.load(input_file)
    
    # Extract paragraph locations
    walker = ParagraphExtractWalker()
    paragraph_map = walker.extract(document)
    
    # Save to file (one verse reference per line)
    with open(output_file, 'w', encoding='utf-8') as f:
        for verse_ref in sorted(paragraph_map.keys()):
            f.write(f"{verse_ref}\n")
    
    print(f"Extracted {len(paragraph_map)} paragraph markers to {output_file}", file=sys.stderr)


def apply_paragraphs(input_file: str, paragraph_file: str, output_file: str):
    """
    Apply paragraph markers from a file to a USFM document.
    
    Args:
        input_file: Path to USFM file
        paragraph_file: Path to paragraph map file
        output_file: Path to save output
    """
    # Load paragraph map from file
    paragraph_map = {}
    with open(paragraph_file, 'r', encoding='utf-8') as f:
        for line in f:
            verse_ref = line.strip()
            if verse_ref:
                paragraph_map[verse_ref] = True
    
    print(f"Loaded {len(paragraph_map)} paragraph markers from {paragraph_file}", file=sys.stderr)
    
    # Parse the USFM file
    parser = UsfmParser()
    document = parser.load(input_file)
    
    # Apply paragraph markers
    walker = ParagraphApplyWalker(paragraph_map)
    modified_document = walker.apply(document)
    
    # Render to Accordance format with paragraph markers
    output_walker = AccordanceWalker(para=True, tc=True)
    output = output_walker.render(modified_document)
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"Applied paragraph markers and saved to {output_file}", file=sys.stderr)


def show_paragraphs(input_file: str):
    """
    Display paragraph marker locations from a USFM file.
    
    Args:
        input_file: Path to USFM file
    """
    # Parse the USFM file
    parser = UsfmParser()
    document = parser.load(input_file)
    
    # Extract paragraph locations
    walker = ParagraphExtractWalker()
    paragraph_map = walker.extract(document)
    
    # Display to stdout
    print(f"Found {len(paragraph_map)} paragraph markers:\n")
    for verse_ref in sorted(paragraph_map.keys()):
        print(verse_ref)


def main():
    """Main entry point for the example script."""
    if len(sys.argv) < 3:
        print("Usage:", file=sys.stderr)
        print("  Extract: python example_paragraphs.py extract <input.usfm> <paragraphs.txt>", file=sys.stderr)
        print("  Apply:   python example_paragraphs.py apply <input.usfm> <paragraphs.txt> <output.acc>", file=sys.stderr)
        print("  Show:    python example_paragraphs.py show <input.usfm>", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print("  # Extract paragraph markers", file=sys.stderr)
        print("  python example_paragraphs.py extract matthew.usfm matt_paragraphs.txt", file=sys.stderr)
        print("\n  # Apply paragraph markers to another file", file=sys.stderr)
        print("  python example_paragraphs.py apply matthew_draft.usfm matt_paragraphs.txt matthew_final.acc", file=sys.stderr)
        print("\n  # Show paragraph locations", file=sys.stderr)
        print("  python example_paragraphs.py show matthew.usfm", file=sys.stderr)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == 'extract':
            if len(sys.argv) != 4:
                print("Error: extract requires <input.usfm> <paragraphs.txt>", file=sys.stderr)
                sys.exit(1)
            input_file = sys.argv[2]
            output_file = sys.argv[3]
            extract_paragraphs(input_file, output_file)
            
        elif command == 'apply':
            if len(sys.argv) != 5:
                print("Error: apply requires <input.usfm> <paragraphs.txt> <output.acc>", file=sys.stderr)
                sys.exit(1)
            input_file = sys.argv[2]
            paragraph_file = sys.argv[3]
            output_file = sys.argv[4]
            apply_paragraphs(input_file, paragraph_file, output_file)
            
        elif command == 'show':
            if len(sys.argv) != 3:
                print("Error: show requires <input.usfm>", file=sys.stderr)
                sys.exit(1)
            input_file = sys.argv[2]
            show_paragraphs(input_file)
            
        else:
            print(f"Error: Unknown command '{command}'", file=sys.stderr)
            print("Valid commands: extract, apply, show", file=sys.stderr)
            sys.exit(1)
            
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
