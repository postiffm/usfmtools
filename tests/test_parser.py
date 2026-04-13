"""
Unit tests for USFM Parser
"""

import pytest
import tempfile
import os
from usfmtools.usfmparser import (
    UsfmParser, Document, Chapter, Verse, Paragraph, Heading,
    Footnote, CrossRef, GlossaryWord, InlineSpan, Text
)


# ============================================================================
# AST Construction Tests
# ============================================================================

def test_parse_simple_book():
    """Test parsing a simple book with one chapter and verse."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 In the beginning"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    assert isinstance(doc, Document)
    assert len(doc.books) == 1
    assert doc.books[0].book_id == "GEN"
    assert len(doc.books[0].children) == 1
    assert isinstance(doc.books[0].children[0], Chapter)
    assert doc.books[0].children[0].number == "1"


def test_parse_multiple_verses():
    """Test parsing multiple verses in a chapter."""
    usfm = r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v 1 First verse" + "\n" + r"\v 2 Second verse"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    chapter = doc.books[0].children[0]
    assert len(chapter.children) == 2
    assert isinstance(chapter.children[0], Verse)
    assert chapter.children[0].number == "1"
    assert isinstance(chapter.children[1], Verse)
    assert chapter.children[1].number == "2"


def test_parse_verse_with_text():
    """Test that verse content is parsed as Text nodes."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 In the beginning God created"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    assert len(verse.children) > 0
    assert isinstance(verse.children[0], Text)
    assert verse.children[0].value == "In"


def test_parse_paragraph_marker():
    """Test parsing paragraph markers."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\p" + "\n" + r"\v 1 Text"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    chapter = doc.books[0].children[0]
    assert len(chapter.children) >= 1
    # Find paragraph marker
    para_found = any(isinstance(child, Paragraph) for child in chapter.children)
    assert para_found


def test_parse_heading():
    """Test parsing heading markers."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\s1 The Creation" + "\n" + r"\v 1 Text"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    chapter = doc.books[0].children[0]
    headings = [child for child in chapter.children if isinstance(child, Heading)]
    assert len(headings) == 1
    assert headings[0].marker == "s1"
    assert "Creation" in headings[0].text


def test_parse_multiple_books():
    """Test parsing multiple books in one document."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text" + "\n" + r"\id EXO" + "\n" + r"\c 1" + "\n" + r"\v 1 More text"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    assert len(doc.books) == 2
    assert doc.books[0].book_id == "GEN"
    assert doc.books[1].book_id == "EXO"


def test_parse_multiple_chapters():
    """Test parsing multiple chapters in a book."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text" + "\n" + r"\c 2" + "\n" + r"\v 1 More text"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    book = doc.books[0]
    chapters = [child for child in book.children if isinstance(child, Chapter)]
    assert len(chapters) == 2
    assert chapters[0].number == "1"
    assert chapters[1].number == "2"


# ============================================================================
# Glossary Word Pipe Delimiter Tests (Requirement 2.3)
# ============================================================================

def test_parse_glossary_word_with_pipe():
    """Test that glossary words extract text before pipe and discard lemma."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 In the \w beginning|lemma\w* God"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    glossary_words = [child for child in verse.children if isinstance(child, GlossaryWord)]
    assert len(glossary_words) == 1
    assert glossary_words[0].word == "beginning"


def test_parse_glossary_word_without_pipe():
    """Test that glossary words without pipe preserve full text."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 In the \w beginning\w* God"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    glossary_words = [child for child in verse.children if isinstance(child, GlossaryWord)]
    assert len(glossary_words) == 1
    assert glossary_words[0].word == "beginning"


def test_parse_glossary_word_with_multiple_pipes():
    """Test that only text before first pipe is extracted."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 \w word|lemma|extra\w*"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    glossary_words = [child for child in verse.children if isinstance(child, GlossaryWord)]
    assert len(glossary_words) == 1
    assert glossary_words[0].word == "word"


def test_parse_glossary_word_multiword():
    """Test glossary word with multiple words before pipe."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 \w two words|lemma\w*"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    glossary_words = [child for child in verse.children if isinstance(child, GlossaryWord)]
    assert len(glossary_words) == 1
    assert glossary_words[0].word == "two words"


# ============================================================================
# Error Cases Tests (Requirements 10.1, 10.3)
# ============================================================================

def test_missing_chapter_number():
    """Test that missing chapter number raises descriptive exception."""
    usfm = r"\id GEN" + "\n" + r"\c" + "\n" + r"\v 1 Text"
    parser = UsfmParser()
    
    with pytest.raises(ValueError) as exc_info:
        parser.loads(usfm, "test.usfm")
    
    assert "Missing chapter number" in str(exc_info.value)
    assert "test.usfm" in str(exc_info.value)


def test_missing_verse_number():
    """Test that missing verse number raises descriptive exception."""
    # When \v is followed by another marker (not text), it should raise an error
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v \p"
    parser = UsfmParser()
    
    with pytest.raises(ValueError) as exc_info:
        parser.loads(usfm, "test.usfm")
    
    assert "Missing verse number" in str(exc_info.value)
    assert "test.usfm" in str(exc_info.value)


def test_missing_book_id():
    """Test that missing book ID raises descriptive exception."""
    usfm = r"\id" + "\n" + r"\c 1"
    parser = UsfmParser()
    
    with pytest.raises(ValueError) as exc_info:
        parser.loads(usfm, "test.usfm")
    
    assert "Missing book ID" in str(exc_info.value)
    assert "test.usfm" in str(exc_info.value)


def test_error_includes_line_number():
    """Test that error messages include line numbers."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text" + "\n" + r"\c"
    parser = UsfmParser()
    
    with pytest.raises(ValueError) as exc_info:
        parser.loads(usfm, "test.usfm")
    
    # Should include line number in error message
    error_msg = str(exc_info.value)
    assert ":" in error_msg  # Format is filename:line


# ============================================================================
# File Loading Tests (Requirements 6.1, 6.2)
# ============================================================================

def test_load_file_with_bom():
    """Test that files with UTF-8 BOM are loaded correctly."""
    usfm_content = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text"
    
    # Create temp file with BOM
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.usfm') as f:
        # Write UTF-8 BOM followed by content
        f.write(b'\xef\xbb\xbf')
        f.write(usfm_content.encode('utf-8'))
        temp_path = f.name
    
    try:
        parser = UsfmParser()
        doc = parser.load(temp_path)
        
        # BOM should not appear in book_id
        assert doc.books[0].book_id == "GEN"
        assert not doc.books[0].book_id.startswith('\ufeff')
    finally:
        os.unlink(temp_path)


def test_load_file_with_crlf():
    """Test that files with Windows line endings are normalized."""
    usfm_content = r"\id GEN" + "\r\n" + r"\c 1" + "\r\n" + r"\v 1 Text"
    
    # Create temp file with CRLF
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.usfm', newline='') as f:
        f.write(usfm_content)
        temp_path = f.name
    
    try:
        parser = UsfmParser()
        doc = parser.load(temp_path)
        
        # Should parse correctly despite CRLF
        assert doc.books[0].book_id == "GEN"
        assert len(doc.books[0].children) == 1
    finally:
        os.unlink(temp_path)


def test_load_file_with_unicode():
    """Test that Unicode characters are preserved."""
    usfm_content = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text with émojis 😊 and accénts"
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.usfm', encoding='utf-8') as f:
        f.write(usfm_content)
        temp_path = f.name
    
    try:
        parser = UsfmParser()
        doc = parser.load(temp_path)
        
        verse = doc.books[0].children[0].children[0]
        # Check that Unicode is preserved in text nodes
        text_content = ' '.join(child.value for child in verse.children if isinstance(child, Text))
        assert '😊' in text_content or 'émojis' in text_content
    finally:
        os.unlink(temp_path)


def test_loads_method():
    """Test that loads() method works with string input."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    assert isinstance(doc, Document)
    assert len(doc.books) == 1


# ============================================================================
# Nested Marker Handling Tests
# ============================================================================

def test_parse_footnote():
    """Test parsing footnotes with nested content."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text \f + \ft footnote text\f* more"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    footnotes = [child for child in verse.children if isinstance(child, Footnote)]
    assert len(footnotes) == 1
    assert len(footnotes[0].children) > 0


def test_parse_crossref():
    """Test parsing cross-references with nested content."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text \x - \xo 1:1 \xt John 1:1\x* more"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    crossrefs = [child for child in verse.children if isinstance(child, CrossRef)]
    assert len(crossrefs) == 1
    assert len(crossrefs[0].children) > 0


def test_parse_inline_span():
    """Test parsing inline character styles."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text \add added text\add* more"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    spans = [child for child in verse.children if isinstance(child, InlineSpan)]
    assert len(spans) == 1
    assert spans[0].marker == "add"
    assert len(spans[0].children) > 0


def test_parse_nested_markers_in_verse():
    """Test multiple nested markers in a single verse."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text \w word|lemma\w* and \add more\add* text"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    assert len(verse.children) > 3  # Should have multiple child nodes
    
    # Check for different node types
    has_glossary = any(isinstance(child, GlossaryWord) for child in verse.children)
    has_span = any(isinstance(child, InlineSpan) for child in verse.children)
    has_text = any(isinstance(child, Text) for child in verse.children)
    
    assert has_glossary
    assert has_span
    assert has_text


def test_parse_poetry_markers():
    """Test parsing poetry paragraph markers."""
    usfm = r"\id PSA" + "\n" + r"\c 1" + "\n" + r"\q1" + "\n" + r"\v 1 First line" + "\n" + r"\q2" + "\n" + r"\v 2 Second line"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    chapter = doc.books[0].children[0]
    paras = [child for child in chapter.children if isinstance(child, Paragraph)]
    assert len(paras) >= 2
    assert any(p.marker == "q1" for p in paras)
    assert any(p.marker == "q2" for p in paras)


def test_parse_list_markers():
    """Test parsing list markers."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\li1" + "\n" + r"\v 1 List item"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    chapter = doc.books[0].children[0]
    paras = [child for child in chapter.children if isinstance(child, Paragraph)]
    assert any(p.marker == "li1" for p in paras)


# ============================================================================
# Edge Cases and Robustness Tests
# ============================================================================

def test_parse_empty_document():
    """Test parsing empty document."""
    usfm = ""
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    assert isinstance(doc, Document)
    assert len(doc.books) == 0


def test_parse_document_without_verses():
    """Test parsing document with only book and chapter markers."""
    usfm = r"\id GEN" + "\n" + r"\c 1"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    assert len(doc.books) == 1
    assert len(doc.books[0].children) == 1
    assert isinstance(doc.books[0].children[0], Chapter)


def test_parse_verse_with_only_markers():
    """Test verse containing only markers and no text."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 \f + \ft note\f*"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    verse = doc.books[0].children[0].children[0]
    assert isinstance(verse, Verse)


def test_parse_book_headers():
    """Test parsing book header markers."""
    usfm = r"\id GEN" + "\n" + r"\h Genesis" + "\n" + r"\toc1 Genesis" + "\n" + r"\c 1" + "\n" + r"\v 1 Text"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    book = doc.books[0]
    headings = [child for child in book.children if isinstance(child, Heading)]
    assert len(headings) >= 1


def test_parse_title_markers():
    """Test parsing title markers."""
    usfm = r"\id GEN" + "\n" + r"\mt1 The Book of Genesis" + "\n" + r"\c 1" + "\n" + r"\v 1 Text"
    parser = UsfmParser()
    doc = parser.loads(usfm)
    
    book = doc.books[0]
    headings = [child for child in book.children if isinstance(child, Heading)]
    assert any(h.marker == "mt1" for h in headings)


def test_debug_mode():
    """Test that debug mode can be enabled without errors."""
    usfm = r"\id GEN" + "\n" + r"\c 1" + "\n" + r"\v 1 Text"
    parser = UsfmParser(debug=True)
    doc = parser.loads(usfm)
    
    assert isinstance(doc, Document)
