"""
USFM Lexer

Tokenizes USFM text into a stream of tokens.
"""

import re
import sys
from dataclasses import dataclass
from typing import List

# Token type constants
TOKEN_MARKER = "MARKER"
TOKEN_MARKER_END = "MARKER_END"
TOKEN_TEXT = "TEXT"


@dataclass
class UsfmToken:
    """
    Represents a single token in the USFM token stream.
    
    Attributes:
        type: Token type (TOKEN_MARKER, TOKEN_MARKER_END, or TOKEN_TEXT)
        value: Marker name (e.g., 'v', 'p') or text content
        line: Source line number for error reporting
    """
    type: str
    value: str
    line: int


# Known USFM markers - single source of truth for supported markers
KNOWN_MARKERS = {
    # Identification
    'id', 'rem', 'h', 'toc1', 'toc2', 'toc3',
    # Titles
    'mt', 'mt1', 'mt2', 'mt3', 'ms', 'imt1', 'imt2',
    # Introductions
    'is', 'ip', 'ipr', 'imq', 'iot', 'io1', 'io2', 'io3', 'ior', 'ie', 'ili',
    # Headings
    's', 's1', 's2', 's3', 'r', 'mr', 'd', 'qa',
    # Chapter and Verse
    'c', 'v',
    # Paragraphs
    'p', 'm', 'mi', 'nb', 'b', 'pi', 'pi2', 'pmo',
    # Poetry
    'q', 'q1', 'q2', 'q3', 'q4', 'qc', 'qs',
    # Lists
    'li', 'li1', 'li2',
    # Footnotes
    'f', 'fr', 'fk', 'ft', 'fw', 'fp',
    # Cross-references
    'x', 'xo', 'xt',
    # Character styles
    'w', 'nd', 'add', 'qt', 'tl', 'rq', 'k',
    # Tables
    'tr', 'th1', 'th2', 'th3', 'tc1', 'tc2', 'tc3',
    # Special
    'periph', '+w',
}


def tokenize(text: str, filename: str = '') -> List[UsfmToken]:
    r"""
    Tokenize USFM text into a stream of tokens.
    
    Args:
        text: Full USFM file content (BOM and CRLF already normalized)
        filename: Optional filename for error messages
        
    Returns:
        List of UsfmToken objects
        
    Behavior:
        - Splits on whitespace to get raw words
        - Scans each word for embedded \marker patterns using regex
        - Handles cases like "justify\w*" → [TEXT('justify'),
          MARKER_END('w')]
        - Handles cases like "\x*cule:" → [MARKER_END('x'),
          TEXT('cule:')]
        - Unknown markers emit TOKEN_MARKER with warning to stderr
        - Content is never silently lost
    """
    tokens = []
    
    # Track current line number by counting newlines
    line_num = 1
    
    # Split text on whitespace to get raw words
    # We need to track position to count newlines properly
    pos = 0
    while pos < len(text):
        # Skip whitespace and count newlines
        while pos < len(text) and text[pos].isspace():
            if text[pos] == '\n':
                line_num += 1
            pos += 1
        
        if pos >= len(text):
            break
        
        # Find the end of the current word (next whitespace)
        word_start = pos
        while pos < len(text) and not text[pos].isspace():
            pos += 1
        
        word = text[word_start:pos]
        
        # Process the word to extract embedded markers
        tokens.extend(_tokenize_word(word, line_num, filename))
    
    return tokens


def _tokenize_word(word: str, line_num: int, filename: str) -> List[UsfmToken]:
    r"""
    Tokenize a single word that may contain embedded markers.
    
    This function handles cases where USFM markers are embedded within
    words, such as "justify\w*" which should become
    [TEXT('justify'), MARKER_END('w')].
    
    Args:
        word: A single whitespace-delimited word
        line_num: Current line number
        filename: Filename for error messages
        
    Returns:
        List of tokens extracted from the word
        
    Examples:
        "justify\w*" → [TEXT('justify'), MARKER_END('w')]
        "\x*cule:" → [MARKER_END('x'), TEXT('cule:')]
        "plain" → [TEXT('plain')]
    """
    tokens = []
    
    # Regex to find USFM markers: backslash followed by alphanumeric/+
    # characters, optionally ending with *
    # Pattern: \marker or \marker*
    # Group 1: marker name (e.g., 'w', 'add', '+w')
    # Group 2: optional asterisk for end markers
    marker_pattern = re.compile(r'\\([a-zA-Z0-9+]+)(\*?)')
    
    pos = 0
    for match in marker_pattern.finditer(word):
        # Emit any text before the marker (e.g., "justify" in "justify\w*")
        if match.start() > pos:
            text_value = word[pos:match.start()]
            tokens.append(UsfmToken(TOKEN_TEXT, text_value, line_num))
        
        # Extract marker name and check if it's an end marker
        marker_name = match.group(1)  # e.g., 'w', 'f', 'x'
        is_end_marker = match.group(2) == '*'  # True if marker ends with *
        
        # Check if marker is known (emit warning but continue processing)
        if marker_name not in KNOWN_MARKERS:
            # Emit warning for unknown marker but preserve content
            location = f" in {filename}" if filename else ""
            warning_msg = (
                f"Warning: Unknown marker '\\{marker_name}{match.group(2)}' "
                f"at line {line_num}{location}"
            )
            print(warning_msg, file=sys.stderr)
        
        # Emit marker token (either opening/standalone or closing)
        if is_end_marker:
            tokens.append(UsfmToken(TOKEN_MARKER_END, marker_name, line_num))
        else:
            tokens.append(UsfmToken(TOKEN_MARKER, marker_name, line_num))
        
        pos = match.end()
    
    # Emit any remaining text after the last marker
    # (e.g., "cule:" in "\x*cule:")
    if pos < len(word):
        text_value = word[pos:]
        tokens.append(UsfmToken(TOKEN_TEXT, text_value, line_num))
    
    return tokens
