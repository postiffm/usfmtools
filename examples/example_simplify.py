#!/usr/bin/env python3
"""
Example: Using SimplifyWalker for Plain Text Output

This script demonstrates how to use the SimplifyWalker to convert USFM files
into plain text suitable for AI training or text analysis. The SimplifyWalker
removes all verse references and markers, producing clean running text.

Usage:
    python example_simplify.py input.usfm > output.txt
"""

import sys
from pathlib import Path

# Add parent directory to path to import usfmtools
sys.path.insert(0, str(Path(__file__).parent.parent))

from usfmtools.usfmparser import UsfmParser
from usfmtools.usfmwalker import SimplifyWalker


def simplify_usfm_file(input_file: str) -> str:
    """
    Convert a USFM file to simplified plain text.
    
    Args:
        input_file: Path to USFM file
        
    Returns:
        Plain text without verse references or markers
    """
    # Parse the USFM file
    parser = UsfmParser()
    document = parser.load(input_file)
    
    # Render using SimplifyWalker
    walker = SimplifyWalker()
    output = walker.render(document)
    
    return output


def main():
    """Main entry point for the example script."""
    if len(sys.argv) < 2:
        print("Usage: python example_simplify.py <input.usfm>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  python example_simplify.py matthew.usfm > matthew_plain.txt", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Check if file exists
    if not Path(input_file).exists():
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Convert to simplified text
        output = simplify_usfm_file(input_file)
        
        # Print to stdout
        print(output)
        
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
