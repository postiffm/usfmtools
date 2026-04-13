"""
USFM Walker - Traverses AST to generate output in various formats.

This module provides walker classes that traverse USFM Abstract Syntax Trees
and generate formatted output. The base UsfmWalker class uses the visitor pattern
to dispatch to node-specific methods.
"""

import sys
from usfmtools.usfmparser import (
    UsfmNode, Document, Book, Chapter, Verse, Paragraph, Heading,
    Footnote, CrossRef, GlossaryWord, InlineSpan, Text, Unknown
)


# ============================================================================
# Base Walker Class
# ============================================================================

class UsfmWalker:
    """
    Base class for AST traversal and output generation.
    Uses visitor pattern to dispatch to node-specific methods.
    """

    def render(self, node: UsfmNode) -> str:
        """
        Render an AST node to string output.

        Args:
            node: AST node to render

        Returns:
            String representation in target format
        """
        method_name = f'visit_{node.__class__.__name__.lower()}'
        method = getattr(self, method_name, self.visit_unknown_node)
        return method(node)

    def visit_document(self, node: Document) -> str:
        """Render document node."""
        return ''.join(self.render(book) for book in node.books)

    def visit_book(self, node: Book) -> str:
        """Render book node."""
        return ''.join(self.render(child) for child in node.children)

    def visit_chapter(self, node: Chapter) -> str:
        """Render chapter node."""
        return ''.join(self.render(child) for child in node.children)

    def visit_verse(self, node: Verse) -> str:
        """Render verse node."""
        return ''.join(self.render(child) for child in node.children)

    def visit_paragraph(self, node: Paragraph) -> str:
        """Render paragraph node."""
        return ''.join(self.render(child) for child in node.children)

    def visit_heading(self, node: Heading) -> str:
        """Render heading node - default: discard."""
        return ''

    def visit_footnote(self, node: Footnote) -> str:
        """Render footnote node - default: discard."""
        return ''

    def visit_crossref(self, node: CrossRef) -> str:
        """Render cross-reference node - default: discard."""
        return ''

    def visit_glossaryword(self, node: GlossaryWord) -> str:
        """Render glossary word - default: emit word only."""
        return node.word

    def visit_inlinespan(self, node: InlineSpan) -> str:
        """Render inline span - default: emit children."""
        return ''.join(self.render(child) for child in node.children)

    def visit_text(self, node: Text) -> str:
        """Render text node."""
        return node.value

    def visit_unknown_node(self, node: UsfmNode) -> str:
        """Render unknown node - warn and emit children if present."""
        print(f"Warning: Unknown node type {node.__class__.__name__}", file=sys.stderr)
        if hasattr(node, 'children'):
            return ''.join(self.render(child) for child in node.children)
        return ''

    def visit_unknown(self, node: Unknown) -> str:
        """Render Unknown AST node."""
        return ''.join(self.render(child) for child in node.children)


# ============================================================================
# AccordanceWalker Class
# ============================================================================

class AccordanceWalker(UsfmWalker):
    """
    Walker that generates Accordance-compatible .acc format.
    """

    # Books to skip (glossaries, front matter, etc.)
    SKIPPED_BOOKS = {
        'GLO', 'XXA', 'XXB', 'FRT', 'XXC', 'XXD', 'INT', 'BAK',
        'XXE', 'XXF', 'XXG', 'CNC', 'TDX', 'OTH', 'TOB', 'JDT',
        'ESG', 'WIS', 'SIR', 'BAR', '1MA', '2MA', '1ES', 'MAN',
        'PS2', '3MA', '2ES', '4MA', 'DAG'
    }

    # Canonical book name mapping
    BOOK_NAMES = {
        "GEN": "Gen.", "EXO": "Ex.", "LEV": "Lev.", "NUM": "Num.",
        "DEU": "Deut.", "JOS": "Josh.", "JDG": "Judg.", "RUT": "Ruth",
        "1SA": "1Sam.", "2SA": "2Sam.", "1KI": "1Kings", "2KI": "2Kings",
        "1CH": "1Chr.", "2CH": "2Chr.", "EZR": "Ezra", "NEH": "Neh.",
        "EST": "Esth.", "JOB": "Job", "PSA": "Psa.", "PRO": "Prov.",
        "ECC": "Eccl.", "SNG": "Song", "ISA": "Is.", "JER": "Jer.",
        "LAM": "Lam.", "EZK": "Ezek.", "DAN": "Dan.", "HOS": "Hos.",
        "JOL": "Joel", "AMO": "Amos", "OBA": "Obad.", "JON": "Jonah",
        "MIC": "Mic.", "NAM": "Nah.", "HAB": "Hab.", "ZEP": "Zeph.",
        "HAG": "Hag.", "ZEC": "Zech.", "MAL": "Mal.", "MAT": "Matt.",
        "MRK": "Mark", "LUK": "Luke", "JHN": "John", "ACT": "Acts",
        "ROM": "Rom.", "1CO": "1Cor.", "2CO": "2Cor.", "GAL": "Gal.",
        "EPH": "Eph.", "PHP": "Phil.", "COL": "Col.", "1TH": "1Th.",
        "2TH": "2Th.", "1TI": "1Tim.", "2TI": "2Tim.", "TIT": "Titus",
        "PHM": "Philem.", "HEB": "Heb.", "JAS": "James", "1PE": "1Pet.",
        "2PE": "2Pet.", "1JN": "1John", "2JN": "2John", "3JN": "3John",
        "JUD": "Jude", "REV": "Rev."
    }

    def __init__(self, para: bool = True, tc: bool = True):
        """
        Initialize Accordance walker.

        Args:
            para: Include paragraph markers (¶) in output
            tc: Include text-critical marks (⸂ and ⸃) in output
        """
        self.para = para
        self.tc = tc
        self.first_verse = True
        self.pending_paragraph = False
        self.current_book = None
        self.current_chapter = None

    def visit_book(self, node: Book) -> str:
        """Render book - skip if in SKIPPED_BOOKS."""
        if node.book_id in self.SKIPPED_BOOKS:
            return ''
        self.current_book = self.BOOK_NAMES.get(node.book_id, node.book_id)
        return ''.join(self.render(child) for child in node.children)

    def visit_chapter(self, node: Chapter) -> str:
        """Render chapter - track chapter number."""
        self.current_chapter = node.number
        return ''.join(self.render(child) for child in node.children)

    def visit_verse(self, node: Verse) -> str:
        """
        Render verse with reference prefix in Accordance format.
        
        Format: "BookName Chapter:Verse¶ text..."
        - First verse in document has no leading newline
        - Subsequent verses start on new lines
        - Paragraph marker (¶) is added if pending_paragraph flag is set
          and para=True
        
        Args:
            node: Verse node to render
            
        Returns:
            Formatted verse with reference and content
        """
        # Format: "Book Chapter:Verse text..."
        # First verse has no leading newline to avoid blank line at start
        # of file
        prefix = '' if self.first_verse else '\n'
        self.first_verse = False

        # Build verse reference (e.g., "Matt. 5:3")
        reference = (
            f"{self.current_book} {self.current_chapter}:{node.number}"
        )

        # Add paragraph marker if pending and para flag is True
        # The pending_paragraph flag is set by visit_paragraph() when a
        # \p marker is encountered
        para_marker = ' ¶' if (self.pending_paragraph and self.para) else ''
        self.pending_paragraph = False  # Reset flag after use

        # Render verse content (text, glossary words, etc.)
        content = ''.join(self.render(child) for child in node.children)
        return f"{prefix}{reference}{para_marker}{content}"

    def visit_paragraph(self, node: Paragraph) -> str:
        """Mark that next verse should have paragraph marker."""
        self.pending_paragraph = True
        return ''.join(self.render(child) for child in node.children)

    def visit_text(self, node: Text) -> str:
        """
        Render text with punctuation spacing rules.
        
        Applies Accordance formatting convention: no space before punctuation.
        This prevents output like "word ." and ensures "word." instead.
        
        Also handles text-critical mark suppression based on tc flag.
        
        Args:
            node: Text node to render
            
        Returns:
            Formatted text with appropriate spacing
        """
        text = node.value

        # Suppress text-critical marks if tc=False
        # Text-critical marks (⸂ and ⸃) indicate textual variants
        if not self.tc:
            # Remove text-critical marks from the text
            text = text.replace('⸂', '').replace('⸃', '')
            # If text is now empty after removing marks, return empty string
            if not text:
                return ''

        # Apply punctuation spacing rule: no space before punctuation
        # This handles cases where punctuation appears as a separate token
        if text and text[0] in '.,:;!?':
            return text  # No leading space

        # Normal text gets a leading space for word separation
        return ' ' + text

    def visit_glossaryword(self, node: GlossaryWord) -> str:
        """Render glossary word with leading space."""
        # Add space before word (unless it starts with punctuation)
        if node.word and node.word[0] in '.,:;!?':
            return node.word
        return ' ' + node.word


# ============================================================================
# SimplifyWalker Class
# ============================================================================

class SimplifyWalker(UsfmWalker):
    """
    Walker that generates plain text output for AI training.
    Similar to AccordanceWalker but without reference prefixes.
    """

    def __init__(self):
        """Initialize simplify walker."""
        pass

    def visit_verse(self, node: Verse) -> str:
        """Render verse content without reference."""
        content = ''.join(self.render(child) for child in node.children)
        return content

    def visit_text(self, node: Text) -> str:
        """Render text with punctuation spacing rules."""
        text = node.value
        if text and text[0] in '.,:;!?':
            return text
        return ' ' + text

    def visit_glossaryword(self, node: GlossaryWord) -> str:
        """Render glossary word with leading space."""
        # Add space before word (unless it starts with punctuation)
        if node.word and node.word[0] in '.,:;!?':
            return node.word
        return ' ' + node.word


# ============================================================================
# ParagraphExtractWalker Class
# ============================================================================

class ParagraphExtractWalker(UsfmWalker):
    """
    Walker that extracts paragraph marker locations.
    Returns dict mapping "BOOK CHAPTER:VERSE" → True for verses with paragraph markers.
    """

    def __init__(self):
        """Initialize paragraph extract walker."""
        self.paragraph_map = {}
        self.current_book = None
        self.current_chapter = None
        self.pending_paragraph = False

    def extract(self, node: Document) -> dict:
        """
        Extract paragraph locations from document.

        Args:
            node: Document node to extract from

        Returns:
            Dict mapping verse references to True
        """
        self.render(node)
        return self.paragraph_map

    def visit_book(self, node: Book) -> str:
        """Track current book."""
        self.current_book = node.book_id
        return super().visit_book(node)

    def visit_chapter(self, node: Chapter) -> str:
        """Track current chapter."""
        self.current_chapter = node.number
        return super().visit_chapter(node)

    def visit_paragraph(self, node: Paragraph) -> str:
        """Mark pending paragraph."""
        self.pending_paragraph = True
        return super().visit_paragraph(node)

    def visit_verse(self, node: Verse) -> str:
        """Record verse if paragraph is pending."""
        if self.pending_paragraph:
            ref = f"{self.current_book} {self.current_chapter}:{node.number}"
            self.paragraph_map[ref] = True
            self.pending_paragraph = False
        return super().visit_verse(node)



# ============================================================================
# ParagraphApplyWalker Class
# ============================================================================

class ParagraphApplyWalker:
    """
    Walker that inserts paragraph markers at specified verse locations.
    Modifies AST in place.
    """

    def __init__(self, paragraph_map: dict):
        """
        Initialize paragraph apply walker.

        Args:
            paragraph_map: Dict mapping verse references to True
        """
        self.paragraph_map = paragraph_map
        self.current_book = None
        self.current_chapter = None

    def apply(self, document: Document) -> Document:
        """
        Apply paragraph markers to document AST.

        Args:
            document: Document node to modify

        Returns:
            Modified document node
        """
        for book in document.books:
            self._process_book(book)
        return document

    def _process_book(self, book: Book) -> None:
        """
        Process a book node, inserting paragraph markers.
        
        Args:
            book: Book node to process (modified in place)
        """
        self.current_book = book.book_id
        for i, child in enumerate(book.children):
            if isinstance(child, Chapter):
                self._process_chapter(child)

    def _process_chapter(self, chapter: Chapter) -> None:
        """
        Process a chapter node, inserting paragraph markers before verses.
        
        This method walks through the chapter's children and inserts
        Paragraph nodes before verses that are marked in the paragraph_map.
        This allows us to reconstruct paragraph structure from a flat list
        of verse references.
        
        Args:
            chapter: Chapter node to process (modified in place)
        """
        self.current_chapter = chapter.number
        new_children = []
        
        for child in chapter.children:
            if isinstance(child, Verse):
                # Check if this verse should have a paragraph marker
                # Build reference in same format as ParagraphExtractWalker
                ref = (
                    f"{self.current_book} "
                    f"{self.current_chapter}:{child.number}"
                )
                if ref in self.paragraph_map:
                    # Insert a Paragraph node before the verse
                    # This will cause AccordanceWalker to set
                    # pending_paragraph flag
                    new_children.append(Paragraph(marker='p', children=[]))
            new_children.append(child)
        
        # Replace chapter's children with new list that includes paragraph
        # markers
        chapter.children = new_children
