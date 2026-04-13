#!/usr/bin/env python3
"""
USFM to Accordance Converter - Command-line interface

Converts USFM (Unified Standard Format Markers) files to Accordance-compatible
import format using the modular lexer → parser → walker architecture.

Usage:
    python usfmToAccordance.py test1.usfm > test1.acc
    python usfmToAccordance.py --no-para --no-tc test3.usfm > test3.acc
    python usfmToAccordance.py *.usfm > combined.acc
"""

import sys
import io
import click
from usfmtools.usfmparser import UsfmParser
from usfmtools.usfmwalker import AccordanceWalker


# Ensure stdout uses UTF-8 encoding on all platforms
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


@click.command()
@click.option(
    '--para/--no-para',
    default=True,
    help='Include paragraph markers (¶) in output. Default: True'
)
@click.option(
    '--tc/--no-tc',
    default=True,
    help='Include text-critical marks (⸂ and ⸃) in output. Default: True'
)
@click.option(
    '--debug/--quiet',
    default=False,
    help='Enable debug output to stderr. Default: False'
)
@click.argument('files', nargs=-1, required=True)
def main(para: bool, tc: bool, debug: bool, files: tuple) -> None:
    """
    Convert USFM files to Accordance-compatible format.
    
    Processes one or more USFM files and outputs the combined result to
    stdout. Error messages and warnings are sent to stderr.
    
    Args:
        para: Include paragraph markers in output
        tc: Include text-critical marks in output
        debug: Enable debug output
        files: Tuple of file paths to process
    """
    parser = UsfmParser(debug=debug)
    walker = AccordanceWalker(para=para, tc=tc)
    
    for filename in files:
        try:
            # Parse the USFM file
            document = parser.load(filename)
            
            # Render to Accordance format
            output = walker.render(document)
            
            # Print to stdout (no trailing newline, walker handles formatting)
            print(output, end='')
            
        except FileNotFoundError:
            print(f"Error: File not found: {filename}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error processing {filename}: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
