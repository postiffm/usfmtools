"""
Unit tests for USFM Lexer

Tests tokenization of USFM text including:
- Basic marker tokenization
- Embedded markers
- Unknown marker warnings
- Line number tracking
- Edge cases
"""

import pytest
import sys
from io import StringIO
from usfmtools.usfmlexer import (
    tokenize,
    UsfmToken,
    TOKEN_MARKER,
    TOKEN_MARKER_END,
    TOKEN_TEXT,
    KNOWN_MARKERS
)


class TestBasicMarkerTokenization:
    """Test basic marker tokenization functionality"""
    
    def test_simple_marker(self):
        """Test tokenizing a simple marker"""
        tokens = tokenize(r'\p')
        assert len(tokens) == 1
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 'p'
        assert tokens[0].line == 1
    
    def test_marker_with_text(self):
        """Test tokenizing marker followed by text"""
        tokens = tokenize(r'\p Hello world')
        assert len(tokens) == 3
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 'p'
        assert tokens[1].type == TOKEN_TEXT
        assert tokens[1].value == 'Hello'
        assert tokens[2].type == TOKEN_TEXT
        assert tokens[2].value == 'world'
    
    def test_multiple_markers(self):
        """Test tokenizing multiple markers"""
        tokens = tokenize(r'\c 1 \v 1')
        assert len(tokens) == 4
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 'c'
        assert tokens[1].type == TOKEN_TEXT
        assert tokens[1].value == '1'
        assert tokens[2].type == TOKEN_MARKER
        assert tokens[2].value == 'v'
        assert tokens[3].type == TOKEN_TEXT
        assert tokens[3].value == '1'
    
    def test_end_marker(self):
        """Test tokenizing end markers with asterisk"""
        tokens = tokenize(r'\w word\w*')
        assert len(tokens) == 3
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 'w'
        assert tokens[1].type == TOKEN_TEXT
        assert tokens[1].value == 'word'
        assert tokens[2].type == TOKEN_MARKER_END
        assert tokens[2].value == 'w'
    
    def test_numbered_markers(self):
        """Test tokenizing markers with numbers"""
        tokens = tokenize(r'\s1 Heading \q2 Poetry')
        assert len(tokens) == 4
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 's1'
        assert tokens[2].type == TOKEN_MARKER
        assert tokens[2].value == 'q2'
    
    def test_special_markers(self):
        """Test tokenizing special markers like +w"""
        tokens = tokenize(r'\+w special')
        assert len(tokens) == 2
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == '+w'


class TestEmbeddedMarkers:
    """Test handling of embedded markers within words"""
    
    def test_embedded_end_marker(self):
        r"""Test word with embedded end marker: word\w*"""
        tokens = tokenize(r'justify\w*')
        assert len(tokens) == 2
        assert tokens[0].type == TOKEN_TEXT
        assert tokens[0].value == 'justify'
        assert tokens[1].type == TOKEN_MARKER_END
        assert tokens[1].value == 'w'
    
    def test_embedded_start_marker(self):
        """Test word with embedded start marker"""
        tokens = tokenize(r'text\w word')
        assert len(tokens) == 3
        assert tokens[0].type == TOKEN_TEXT
        assert tokens[0].value == 'text'
        assert tokens[1].type == TOKEN_MARKER
        assert tokens[1].value == 'w'
        assert tokens[2].type == TOKEN_TEXT
        assert tokens[2].value == 'word'
    
    def test_marker_at_start_with_text(self):
        r"""Test marker at start of word with trailing text: \x*cule:"""
        tokens = tokenize(r'\x*cule:')
        assert len(tokens) == 2
        assert tokens[0].type == TOKEN_MARKER_END
        assert tokens[0].value == 'x'
        assert tokens[1].type == TOKEN_TEXT
        assert tokens[1].value == 'cule:'
    
    def test_multiple_embedded_markers(self):
        r"""Test word with multiple embedded markers"""
        tokens = tokenize(r'text\w word\w*more')
        assert len(tokens) == 5
        assert tokens[0].type == TOKEN_TEXT
        assert tokens[0].value == 'text'
        assert tokens[1].type == TOKEN_MARKER
        assert tokens[1].value == 'w'
        assert tokens[2].type == TOKEN_TEXT
        assert tokens[2].value == 'word'
        assert tokens[3].type == TOKEN_MARKER_END
        assert tokens[3].value == 'w'
        assert tokens[4].type == TOKEN_TEXT
        assert tokens[4].value == 'more'
    
    def test_embedded_marker_with_punctuation(self):
        r"""Test embedded marker followed by punctuation"""
        tokens = tokenize(r'word\w*.')
        assert len(tokens) == 3
        assert tokens[0].type == TOKEN_TEXT
        assert tokens[0].value == 'word'
        assert tokens[1].type == TOKEN_MARKER_END
        assert tokens[1].value == 'w'
        assert tokens[2].type == TOKEN_TEXT
        assert tokens[2].value == '.'


class TestUnknownMarkerWarnings:
    """Test warning behavior for unknown markers"""
    
    def test_unknown_marker_warning(self, capsys):
        """Test that unknown markers emit warnings to stderr"""
        tokens = tokenize(r'\unknown test')
        
        # Check that token is still created
        assert len(tokens) == 2
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 'unknown'
        
        # Check warning was emitted to stderr
        captured = capsys.readouterr()
        assert 'Warning: Unknown marker' in captured.err
        assert 'unknown' in captured.err
        assert 'line 1' in captured.err
    
    def test_unknown_marker_with_filename(self, capsys):
        """Test that unknown marker warnings include filename"""
        tokens = tokenize(r'\badmarker text', filename='test.usfm')
        
        # Check warning includes filename
        captured = capsys.readouterr()
        assert 'test.usfm' in captured.err
        assert 'badmarker' in captured.err
    
    def test_unknown_end_marker_warning(self, capsys):
        r"""Test that unknown end markers emit warnings"""
        tokens = tokenize(r'\xyz*')
        
        # Check that token is still created
        assert len(tokens) == 1
        assert tokens[0].type == TOKEN_MARKER_END
        assert tokens[0].value == 'xyz'
        
        # Check warning was emitted
        captured = capsys.readouterr()
        assert 'Warning: Unknown marker' in captured.err
        assert 'xyz*' in captured.err
    
    def test_content_preserved_with_unknown_marker(self):
        """Test that content is never lost even with unknown markers"""
        tokens = tokenize(r'\unknown before \p after')
        
        # All content should be tokenized
        assert len(tokens) == 4
        assert tokens[0].value == 'unknown'
        assert tokens[1].value == 'before'
        assert tokens[2].value == 'p'
        assert tokens[3].value == 'after'
    
    def test_known_markers_no_warning(self, capsys):
        """Test that known markers don't emit warnings"""
        # Test a sample of known markers
        tokens = tokenize(r'\p \v \c \s1 \w \f \x')
        
        # No warnings should be emitted
        captured = capsys.readouterr()
        assert captured.err == ''


class TestLineNumberTracking:
    """Test line number tracking across multi-line input"""
    
    def test_single_line(self):
        """Test line numbers on single line"""
        tokens = tokenize(r'\p word1 word2')
        assert all(token.line == 1 for token in tokens)
    
    def test_multiple_lines(self):
        """Test line numbers across multiple lines"""
        text = r'''\p line one
\v 1 line two
\v 2 line three'''
        tokens = tokenize(text)
        
        # First line tokens
        assert tokens[0].line == 1  # \p
        assert tokens[1].line == 1  # line
        assert tokens[2].line == 1  # one
        
        # Second line tokens
        assert tokens[3].line == 2  # \v
        assert tokens[4].line == 2  # 1
        assert tokens[5].line == 2  # line
        assert tokens[6].line == 2  # two
        
        # Third line tokens
        assert tokens[7].line == 3  # \v
        assert tokens[8].line == 3  # 2
        assert tokens[9].line == 3  # line
        assert tokens[10].line == 3  # three
    
    def test_empty_lines(self):
        """Test line number tracking with empty lines"""
        text = r'''\p first

\v 1 third'''
        tokens = tokenize(text)
        
        assert tokens[0].line == 1  # \p
        assert tokens[1].line == 1  # first
        assert tokens[2].line == 3  # \v (line 2 is empty)
        assert tokens[3].line == 3  # 1
        assert tokens[4].line == 3  # third
    
    def test_line_numbers_with_embedded_markers(self):
        r"""Test line numbers are correct with embedded markers"""
        text = r'''word\w*
next\w line'''
        tokens = tokenize(text)
        
        assert tokens[0].line == 1  # word
        assert tokens[1].line == 1  # \w*
        assert tokens[2].line == 2  # next
        assert tokens[3].line == 2  # \w
        assert tokens[4].line == 2  # line
    
    def test_many_lines(self):
        """Test line number tracking across many lines"""
        lines = [r'\p line' for _ in range(100)]
        text = '\n'.join(lines)
        tokens = tokenize(text)
        
        # Check every 10th line
        for i in range(0, 100, 10):
            # Each line has 2 tokens: \p, line
            # Line i has tokens at positions i*2, i*2+1
            token_index = i * 2
            assert tokens[token_index].line == i + 1, f"Token at index {token_index} should be on line {i+1}, but is on line {tokens[token_index].line}"


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_empty_input(self):
        """Test tokenizing empty string"""
        tokens = tokenize('')
        assert tokens == []
    
    def test_whitespace_only(self):
        """Test tokenizing whitespace-only input"""
        tokens = tokenize('   \n\t  \n  ')
        assert tokens == []
    
    def test_single_word(self):
        """Test tokenizing single word without markers"""
        tokens = tokenize('word')
        assert len(tokens) == 1
        assert tokens[0].type == TOKEN_TEXT
        assert tokens[0].value == 'word'
    
    def test_marker_only(self):
        """Test tokenizing single marker"""
        tokens = tokenize(r'\p')
        assert len(tokens) == 1
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 'p'
    
    def test_multiple_spaces(self):
        """Test that multiple spaces are handled correctly"""
        tokens = tokenize(r'\p    word1     word2')
        assert len(tokens) == 3
        assert tokens[0].value == 'p'
        assert tokens[1].value == 'word1'
        assert tokens[2].value == 'word2'
    
    def test_tabs_and_spaces(self):
        """Test mixed whitespace handling"""
        tokens = tokenize('\t\\p\t\tword1\n\t\\v\t1')
        assert len(tokens) == 4
        assert tokens[0].value == 'p'
        assert tokens[1].value == 'word1'
        assert tokens[2].value == 'v'
        assert tokens[3].value == '1'
    
    def test_punctuation_only(self):
        """Test tokenizing punctuation"""
        tokens = tokenize('.')
        assert len(tokens) == 1
        assert tokens[0].type == TOKEN_TEXT
        assert tokens[0].value == '.'
    
    def test_numbers_only(self):
        """Test tokenizing numbers"""
        tokens = tokenize('123 456')
        assert len(tokens) == 2
        assert tokens[0].value == '123'
        assert tokens[1].value == '456'
    
    def test_unicode_text(self):
        """Test tokenizing Unicode characters"""
        tokens = tokenize(r'\p καὶ ἐγένετο')
        assert len(tokens) == 3
        assert tokens[0].value == 'p'
        assert tokens[1].value == 'καὶ'
        assert tokens[2].value == 'ἐγένετο'
    
    def test_special_unicode_marks(self):
        """Test tokenizing special Unicode marks like text-critical marks"""
        tokens = tokenize(r'\p text ⸂critical⸃ more')
        assert len(tokens) == 4
        assert tokens[1].value == 'text'
        assert tokens[2].value == '⸂critical⸃'
        assert tokens[3].value == 'more'
    
    def test_backslash_without_marker(self):
        """Test backslash not followed by valid marker characters"""
        # Backslash followed by space should be treated as text
        tokens = tokenize(r'\ word')
        # The backslash alone won't match the marker pattern
        assert len(tokens) == 2
        assert tokens[0].type == TOKEN_TEXT
        assert tokens[0].value == '\\'
        assert tokens[1].value == 'word'
    
    def test_consecutive_markers(self):
        r"""Test consecutive markers without text between"""
        tokens = tokenize(r'\p\v')
        assert len(tokens) == 2
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 'p'
        assert tokens[1].type == TOKEN_MARKER
        assert tokens[1].value == 'v'


class TestRealWorldExamples:
    """Test realistic USFM examples"""
    
    def test_verse_with_glossary_word(self):
        r"""Test verse with glossary word containing pipe delimiter"""
        tokens = tokenize(r'\v 1 In the beginning \w God|G2316\w* created')
        
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 'v'
        assert tokens[1].type == TOKEN_TEXT
        assert tokens[1].value == '1'
        assert tokens[2].type == TOKEN_TEXT
        assert tokens[2].value == 'In'
        # ... more text tokens ...
        # Find the \w marker
        w_marker_idx = next(i for i, t in enumerate(tokens) if t.value == 'w' and t.type == TOKEN_MARKER)
        assert tokens[w_marker_idx + 1].value == 'God|G2316'
        # Find the \w* end marker
        w_end_idx = next(i for i, t in enumerate(tokens) if t.value == 'w' and t.type == TOKEN_MARKER_END)
        assert tokens[w_end_idx].type == TOKEN_MARKER_END
    
    def test_footnote_structure(self):
        r"""Test footnote with internal markers"""
        tokens = tokenize(r'\v 1 Text\f + \fr 1.1 \ft Note text\f* more')
        
        # Verify structure
        assert any(t.value == 'v' and t.type == TOKEN_MARKER for t in tokens)
        assert any(t.value == 'f' and t.type == TOKEN_MARKER for t in tokens)
        assert any(t.value == 'fr' and t.type == TOKEN_MARKER for t in tokens)
        assert any(t.value == 'ft' and t.type == TOKEN_MARKER for t in tokens)
        assert any(t.value == 'f' and t.type == TOKEN_MARKER_END for t in tokens)
    
    def test_poetry_paragraph(self):
        """Test poetry paragraph markers"""
        text = r'''\q1 First line
\q2 Second line indented
\q1 Third line'''
        tokens = tokenize(text)
        
        # Find all q markers
        q_markers = [t for t in tokens if t.value in ('q1', 'q2') and t.type == TOKEN_MARKER]
        assert len(q_markers) == 3
        assert q_markers[0].value == 'q1'
        assert q_markers[1].value == 'q2'
        assert q_markers[2].value == 'q1'
    
    def test_chapter_and_verse(self):
        """Test chapter and verse markers"""
        text = r'''\c 1
\v 1 First verse
\v 2 Second verse'''
        tokens = tokenize(text)
        
        assert tokens[0].type == TOKEN_MARKER
        assert tokens[0].value == 'c'
        assert tokens[1].value == '1'
        assert tokens[2].type == TOKEN_MARKER
        assert tokens[2].value == 'v'
        assert tokens[3].value == '1'
