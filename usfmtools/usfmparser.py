"""
USFM Parser - Converts token streams into Abstract Syntax Trees.

This module provides the UsfmParser class and AST node definitions for parsing
USFM (Unified Standard Format Markers) files into a structured tree representation.
"""

from dataclasses import dataclass, field
from typing import List, Union, Optional
import sys
from usfmtools.usfmlexer import tokenize, UsfmToken, TOKEN_MARKER, TOKEN_MARKER_END, TOKEN_TEXT


# ============================================================================
# AST Node Classes
# ============================================================================

class UsfmNode:
    """Base class for all AST nodes."""
    pass


@dataclass
class Document(UsfmNode):
    """Root node containing all books."""
    books: List['Book'] = field(default_factory=list)


@dataclass
class Book(UsfmNode):
    """Represents a single Bible book."""
    book_id: str  # Three-letter code: 'MAT', 'GEN', etc.
    # Headers, chapters
    children: List[UsfmNode] = field(default_factory=list)


@dataclass
class Chapter(UsfmNode):
    """Represents a chapter within a book."""
    number: str
    # Paragraphs, verses, headings
    children: List[UsfmNode] = field(default_factory=list)


@dataclass
class Verse(UsfmNode):
    """Represents a verse within a chapter."""
    number: str
    # Inline content
    children: List[UsfmNode] = field(default_factory=list)


@dataclass
class Paragraph(UsfmNode):
    """Paragraph marker (p, m, q1, pi, etc.)."""
    marker: str  # 'p', 'm', 'q1', 'pi', etc.
    children: List[UsfmNode] = field(default_factory=list)


@dataclass
class Heading(UsfmNode):
    """Section heading or title."""
    marker: str  # 's1', 's2', 'h', 'mt1', etc.
    text: str


@dataclass
class Footnote(UsfmNode):
    """Footnote content (usually discarded by walkers)."""
    # fr, ft, fk content
    children: List[UsfmNode] = field(default_factory=list)


@dataclass
class CrossRef(UsfmNode):
    """Cross-reference content (usually discarded by walkers)."""
    # xo, xt content
    children: List[UsfmNode] = field(default_factory=list)


@dataclass
class GlossaryWord(UsfmNode):
    """Word with glossary/lexical information."""
    word: str  # Text before | (or full text if no |)
    # Note: lemma form (after |) is discarded at parse time


@dataclass
class InlineSpan(UsfmNode):
    """Inline character style (add, nd, qt, tl, rq, etc.)."""
    marker: str
    children: List[UsfmNode] = field(default_factory=list)


@dataclass
class Text(UsfmNode):
    """Plain text content."""
    value: str


@dataclass
class Unknown(UsfmNode):
    """Unknown marker - content preserved with warning."""
    marker: str
    children: List[UsfmNode] = field(default_factory=list)



# ============================================================================
# Parser Class
# ============================================================================

class UsfmParser:
    """
    Parses USFM token streams into Abstract Syntax Trees.
    """

    def __init__(self, debug: bool = False):
        """
        Initialize parser.

        Args:
            debug: Enable debug output to stderr
        """
        self.debug = debug
        self.tokens = []
        self.pos = 0
        self.marker_stack = []
        self.filename = ''

    def load(self, filename: str) -> Document:
        """
        Load and parse a USFM file.

        Args:
            filename: Path to USFM file

        Returns:
            Document node (root of AST)

        Behavior:
            - Opens with encoding='utf-8-sig' to strip BOM
            - Normalizes \\r\\n → \\n
            - Calls loads() with file content
        """
        with open(filename, 'r', encoding='utf-8-sig') as f:
            text = f.read()
        # Normalize line endings
        text = text.replace('\r\n', '\n')
        return self.loads(text, filename)

    def loads(self, text: str, filename: str = '') -> Document:
        """
        Parse USFM text into an AST.

        Args:
            text: USFM content as string
            filename: Optional filename for error messages

        Returns:
            Document node (root of AST)
        """
        self.filename = filename
        self.tokens = tokenize(text, filename)
        self.pos = 0
        self.marker_stack = []

        return self._parse_document()


    # ========================================================================
    # Helper Methods
    # ========================================================================

    def _current_token(self) -> Optional[UsfmToken]:
        """Get current token without advancing."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _peek_token(self, offset: int = 1) -> Optional[UsfmToken]:
        """Peek ahead at token without advancing."""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def _advance(self) -> Optional[UsfmToken]:
        """Consume and return current token."""
        token = self._current_token()
        if token:
            self.pos += 1
        return token

    def _expect_text(self, context: str) -> str:
        """
        Expect a TEXT token and return its value.
        Raises exception if not found.
        """
        token = self._current_token()
        if not token or token.type != TOKEN_TEXT:
            line = token.line if token else 'EOF'
            raise ValueError(f"{context} in {self.filename}:{line}")
        return self._advance().value

    # ========================================================================
    # Parsing Methods
    # ========================================================================

    def _parse_document(self) -> Document:
        """Parse entire document into books."""
        doc = Document()

        while self._current_token():
            token = self._current_token()

            if token.type == TOKEN_MARKER:
                if token.value == 'id':
                    # Start of a new book
                    book = self._parse_book()
                    doc.books.append(book)
                else:
                    # Skip markers before first book
                    self._advance()
            else:
                # Skip text before first book
                self._advance()

        return doc

    def _parse_book(self) -> Book:
        """Parse a book starting from \\id marker."""
        # Consume \\id marker
        self._advance()

        # Get book ID (e.g., 'MAT', 'GEN')
        book_id = self._expect_text("Missing book ID after \\id")

        book = Book(book_id=book_id.strip())

        # Parse book content until next \\id or EOF
        while self._current_token():
            token = self._current_token()

            # Stop at next book
            if token.type == TOKEN_MARKER and token.value == 'id':
                break

            if token.type == TOKEN_MARKER:
                if token.value == 'c':
                    # Chapter marker
                    chapter = self._parse_chapter()
                    book.children.append(chapter)
                elif token.value in ('h', 'toc1', 'toc2', 'toc3', 'mt', 'mt1', 'mt2', 'mt3', 'ms', 'imt1', 'imt2'):
                    # Heading/title markers
                    heading = self._parse_heading()
                    book.children.append(heading)
                else:
                    # Other markers - skip for now
                    self._advance()
            else:
                # Skip text outside chapters
                self._advance()

        return book

    def _parse_chapter(self) -> Chapter:
        """Parse a chapter starting from \\c marker."""
        # Consume \\c marker
        self._advance()

        # Get chapter number
        chapter_num = self._expect_text("Missing chapter number after \\c")

        chapter = Chapter(number=chapter_num.strip())

        # Parse chapter content until next \\c or \\id or EOF
        while self._current_token():
            token = self._current_token()

            # Stop at next chapter or book
            if token.type == TOKEN_MARKER and token.value in ('c', 'id'):
                break

            if token.type == TOKEN_MARKER:
                if token.value == 'v':
                    # Verse marker
                    verse = self._parse_verse()
                    chapter.children.append(verse)
                elif token.value in ('p', 'm', 'mi', 'nb', 'b', 'pi', 'pi2', 'pmo', 'q', 'q1', 'q2', 'q3', 'q4', 'qc', 'qs', 'li', 'li1', 'li2'):
                    # Paragraph markers
                    para = self._parse_paragraph()
                    chapter.children.append(para)
                elif token.value in ('s', 's1', 's2', 's3', 'r', 'mr', 'd', 'qa', 'is', 'ip', 'ipr', 'imq', 'iot', 'io1', 'io2', 'io3', 'ior', 'ie', 'ili'):
                    # Heading markers
                    heading = self._parse_heading()
                    chapter.children.append(heading)
                else:
                    # Other markers - skip
                    self._advance()
            else:
                # Skip text outside verses
                self._advance()

        return chapter

    def _parse_verse(self) -> Verse:
        """
        Parse a verse starting from \\v marker.
        
        Verses contain inline content (text, glossary words, footnotes, etc.)
        and end when we encounter the next verse, chapter, book, or section heading.
        
        Special handling for paragraph markers: If a paragraph marker is immediately
        followed by a verse marker, it belongs to the next verse, not this one.
        
        Returns:
            Verse node with all inline content as children
        """
        # Consume \\v marker
        self._advance()

        # Get verse number (required - will raise exception if missing)
        verse_num = self._expect_text("Missing verse number after \\v")

        verse = Verse(number=verse_num.strip())

        # Parse verse content until next structural marker
        while self._current_token():
            token = self._current_token()

            # Stop at next verse, chapter, or book (structural boundaries)
            if token.type == TOKEN_MARKER and token.value in ('v', 'c', 'id'):
                break
            
            # Stop at section headings (these truly end a verse)
            if token.type == TOKEN_MARKER and token.value in ('s', 's1', 's2', 's3', 'r', 'mr', 'd', 'qa'):
                break

            # Handle paragraph/poetry markers with lookahead:
            # These markers can appear either:
            # 1. Before a verse (indicating the verse starts a new paragraph)
            # 2. Within a verse (just formatting, should be skipped)
            # We use lookahead to distinguish these cases.
            if token.type == TOKEN_MARKER and token.value in ('p', 'm', 'mi', 'nb', 'b', 'pi', 'pi2', 'pmo', 'q', 'q1', 'q2', 'q3', 'q4', 'qc', 'qs', 'li', 'li1', 'li2'):
                # Look ahead to see if next token is a verse marker
                next_idx = self.pos + 1
                if next_idx < len(self.tokens):
                    next_token = self.tokens[next_idx]
                    if (next_token.type == TOKEN_MARKER and
                            next_token.value == 'v'):
                        # Pattern: \p \v N means paragraph belongs to
                        # verse N, not current verse
                        # Stop here so the paragraph marker is available
                        # for the next verse
                        break
                # Not followed by verse marker, so it's just formatting
                # within this verse. Skip it and continue collecting
                # verse content
                self._advance()
                continue

            # Parse inline content (text, glossary words, footnotes, etc.)
            node = self._parse_inline_content()
            if node:
                verse.children.append(node)

        return verse

    def _parse_paragraph(self) -> Paragraph:
        """Parse a paragraph marker."""
        token = self._advance()
        return Paragraph(marker=token.value)

    def _parse_heading(self) -> Heading:
        """Parse a heading marker and its text."""
        marker_token = self._advance()
        marker = marker_token.value

        # Collect text until next marker or EOL
        text_parts = []
        while self._current_token():
            token = self._current_token()
            if token.type == TOKEN_MARKER:
                break
            text_parts.append(self._advance().value)

        return Heading(marker=marker, text=' '.join(text_parts))

    def _parse_inline_content(self) -> Optional[UsfmNode]:
        """Parse inline content within a verse."""
        token = self._current_token()
        if not token:
            return None

        if token.type == TOKEN_TEXT:
            return Text(value=self._advance().value)

        elif token.type == TOKEN_MARKER:
            marker = token.value

            if marker == 'w':
                return self._parse_glossary_word()
            elif marker == 'f':
                return self._parse_footnote()
            elif marker == 'x':
                return self._parse_crossref()
            elif marker in ('nd', 'add', 'qt', 'tl', 'rq', 'k', '+w'):
                return self._parse_inline_span()
            else:
                # Unknown inline marker
                self._advance()
                return Unknown(marker=marker)

        elif token.type == TOKEN_MARKER_END:
            # End marker without matching start - skip
            self._advance()
            return None

        return None

    def _parse_glossary_word(self) -> GlossaryWord:
        """
        Parse glossary word with pipe delimiter handling.
        
        Glossary words in USFM can have the format: \\w word|lemma\\w*
        where "word" is the display text and "lemma" is the lexical form.
        We extract only the word portion and discard the lemma.
        
        Examples:
            \\w justify|δικαιόω\\w* → GlossaryWord(word='justify')
            \\w grace\\w* → GlossaryWord(word='grace')
        
        Returns:
            GlossaryWord node with only the word portion (before pipe)
        """
        # Consume \\w marker
        self._advance()

        # Collect content until \\w* end marker
        content_parts = []
        while self._current_token():
            token = self._current_token()
            if token.type == TOKEN_MARKER_END and token.value == 'w':
                self._advance()  # Consume \\w*
                break
            if token.type == TOKEN_TEXT:
                content_parts.append(self._advance().value)
            else:
                self._advance()

        # Join content and extract word before pipe delimiter
        full_content = ' '.join(content_parts)
        if '|' in full_content:
            # Split on pipe: take only the part before | (the display word)
            # Discard the part after | (the lemma/lexical form)
            word = full_content.split('|')[0].strip()
        else:
            # No pipe delimiter, use entire content
            word = full_content.strip()

        return GlossaryWord(word=word)

    def _parse_footnote(self) -> Footnote:
        """Parse footnote content."""
        # Consume \\f marker
        self._advance()

        footnote = Footnote()

        # Collect content until \\f*
        while self._current_token():
            token = self._current_token()
            if token.type == TOKEN_MARKER_END and token.value == 'f':
                self._advance()  # Consume \\f*
                break

            if token.type == TOKEN_TEXT:
                footnote.children.append(Text(value=self._advance().value))
            elif token.type == TOKEN_MARKER:
                # Footnote sub-markers (fr, ft, fk, etc.) - just collect as text
                self._advance()
            else:
                self._advance()

        return footnote

    def _parse_crossref(self) -> CrossRef:
        """Parse cross-reference content."""
        # Consume \\x marker
        self._advance()

        crossref = CrossRef()

        # Collect content until \\x*
        while self._current_token():
            token = self._current_token()
            if token.type == TOKEN_MARKER_END and token.value == 'x':
                self._advance()  # Consume \\x*
                break

            if token.type == TOKEN_TEXT:
                crossref.children.append(Text(value=self._advance().value))
            elif token.type == TOKEN_MARKER:
                # Cross-ref sub-markers (xo, xt, etc.) - just collect as text
                self._advance()
            else:
                self._advance()

        return crossref

    def _parse_inline_span(self) -> InlineSpan:
        """Parse inline character style span."""
        marker_token = self._advance()
        marker = marker_token.value

        span = InlineSpan(marker=marker)

        # Collect content until matching end marker
        while self._current_token():
            token = self._current_token()
            if token.type == TOKEN_MARKER_END and token.value == marker:
                self._advance()  # Consume end marker
                break

            if token.type == TOKEN_TEXT:
                span.children.append(Text(value=self._advance().value))
            else:
                self._advance()

        return span
