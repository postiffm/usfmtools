# Implementation Plan: USFM Parser Refactor

## Overview

This plan implements a clean three-stage compiler architecture (Lexer → Parser → Walker) to replace the existing monolithic USFM parser. The implementation follows the migration path: lexer → parser → AccordanceWalker → test compatibility → SimplifyWalker → paragraph walkers → property tests → documentation.

## Tasks

- [x] 1. Set up project structure and core modules
  - Create `usfmtools/` directory for the new implementation
  - Create empty module files: `usfmlexer.py`, `usfmparser.py`, `usfmwalker.py`
  - Create `tests/` directory with empty test files
  - Set up pytest configuration if needed
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 2. Implement lexer component
  - [x] 2.1 Define token types and UsfmToken dataclass
    - Create TOKEN_MARKER, TOKEN_MARKER_END, TOKEN_TEXT constants
    - Implement UsfmToken dataclass with type, value, and line fields
    - _Requirements: 1.1, 1.5_
  
  - [x] 2.2 Define KNOWN_MARKERS set
    - Add all supported USFM markers from requirements (identification, titles, introductions, headings, chapter/verse, paragraphs, poetry, lists, footnotes, cross-references, character styles, tables, special markers)
    - _Requirements: 1.2, 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.13_
  
  - [x] 2.3 Implement tokenize() function
    - Split input text on whitespace to get raw words
    - Use regex to find embedded markers within words
    - Classify markers as MARKER or MARKER_END (markers ending with *)
    - Track line numbers by counting newlines
    - Emit warnings to stderr for unknown markers but preserve content
    - _Requirements: 1.1, 1.3, 1.4, 1.5, 10.2, 10.4_
  
  - [x] 2.4 Write unit tests for lexer
    - Test basic marker tokenization
    - Test embedded markers (e.g., "word\w*")
    - Test unknown marker warnings
    - Test line number tracking
    - Test edge cases (empty input, whitespace-only)
    - _Requirements: 1.1, 1.3, 1.4, 1.5_

- [x] 3. Implement parser component
  - [x] 3.1 Define AST node classes
    - Create base UsfmNode class
    - Implement dataclasses for: Document, Book, Chapter, Verse, Paragraph, Heading, Footnote, CrossRef, GlossaryWord, InlineSpan, Text, Unknown
    - Each node should have appropriate fields (e.g., children lists, marker names, text content)
    - _Requirements: 2.1_
  
  - [x] 3.2 Implement UsfmParser class with load() and loads() methods
    - Implement load() to read file with utf-8-sig encoding and normalize line endings
    - Implement loads() to parse text string into AST
    - _Requirements: 2.4, 2.5, 6.1, 6.2, 6.3_
  
  - [x] 3.3 Implement parsing logic with marker stack
    - Initialize token cursor and marker stack
    - Use recursive descent parsing for document → books → chapters → verses
    - Track open markers on stack to handle nesting correctly
    - Handle glossary words with pipe delimiters (extract word before |, discard lemma after |)
    - Raise descriptive exceptions for missing chapter/verse numbers with filename and line number
    - _Requirements: 2.2, 2.3, 10.1, 10.3_
  
  - [x] 3.4 Write unit tests for parser
    - Test AST construction for various USFM structures
    - Test glossary word pipe delimiter extraction
    - Test error cases (missing chapter/verse numbers)
    - Test file loading with BOM and different line endings
    - Test nested marker handling
    - _Requirements: 2.1, 2.3, 6.1, 6.2, 10.1, 10.3_

- [x] 4. Checkpoint - Ensure lexer and parser tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement base walker and AccordanceWalker
  - [x] 5.1 Implement base UsfmWalker class
    - Create render() method that dispatches to visit_* methods
    - Implement visit methods for all AST node types with default behaviors
    - _Requirements: 3.1, 3.5_
  
  - [x] 5.2 Implement AccordanceWalker class
    - Define SKIPPED_BOOKS and BOOK_NAMES constants
    - Implement constructor with para and tc flags
    - Implement visit_book() to skip books in SKIPPED_BOOKS
    - Implement visit_chapter() to track current chapter
    - Implement visit_verse() to format "BookName Chapter:Verse" with optional ¶ marker
    - Implement visit_paragraph() to set pending_paragraph flag
    - Implement visit_text() with punctuation spacing rules and tc flag handling
    - Implement visit_glossaryword() to emit word with spacing
    - Implement visit_footnote() and visit_crossref() to discard content
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_
  
  - [x] 5.3 Write unit tests for AccordanceWalker
    - Test verse format output
    - Test paragraph marker insertion with para flag
    - Test text-critical mark suppression with tc flag
    - Test footnote and cross-reference filtering
    - Test punctuation spacing rules
    - Test skipped book filtering
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

- [x] 6. Implement command-line interface
  - [x] 6.1 Create usfmToAccordance.py CLI script
    - Use click library for argument parsing
    - Add --para/--no-para flag (default True)
    - Add --tc/--no-tc flag (default True)
    - Add --debug/--quiet flag (default False)
    - Accept multiple file arguments
    - Process files and output to stdout
    - Handle errors gracefully with error messages to stderr
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_
  
  - [x] 6.2 Write integration tests for CLI
    - Test single file processing
    - Test multiple file processing
    - Test flag behavior (--para, --tc, --debug)
    - Test error handling with pytest
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 7. Run existing test suite and fix discrepancies
  - Create pytest-based integration tests that compare output with reference test[1-n].acc files
  - Run tests against new implementation
  - Fix any discrepancies (should match byte-for-byte or be justified bug fixes)
  - Document any intentional output changes
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 8. Checkpoint - Ensure backward compatibility
  - Ensure all tests pass, ask the user if questions arise.

- [x] 9. Implement SimplifyWalker for AI training
  - [x] 9.1 Create SimplifyWalker class
    - Implement visit_verse() to render content without reference prefix
    - Implement visit_text() with punctuation spacing rules
    - Reuse base walker methods for other node types
    - _Requirements: 3.3, 11.1_
  
  - [x] 9.2 Write unit tests for SimplifyWalker
    - Test plain text output without verse references
    - Test punctuation spacing
    - Test that footnotes and cross-references are filtered
    - _Requirements: 3.3_

- [x] 10. Implement paragraph extract and apply walkers
  - [x] 10.1 Create ParagraphExtractWalker class
    - Implement extract() method that returns dict mapping verse references to True
    - Track current book and chapter as traversing AST
    - Record verses preceded by paragraph markers
    - _Requirements: 11.3_
  
  - [x] 10.2 Create ParagraphApplyWalker class
    - Implement apply() method that modifies AST in place
    - Insert Paragraph nodes before verses in paragraph_map
    - _Requirements: 11.4_
  
  - [x] 10.3 Write unit tests for paragraph walkers
    - Test paragraph extraction from sample AST
    - Test paragraph application to sample AST
    - Test round-trip (extract then apply)
    - _Requirements: 11.3, 11.4_

- [x] 11. Add code quality improvements
  - [x] 11.1 Add docstrings to all public classes and functions
    - Document parameters, return values, and behavior
    - _Requirements: 9.2_
  
  - [x] 11.2 Add type hints to all functions
    - Use Python type hints for parameters and return values
    - _Requirements: 9.4_
  
  - [x] 11.3 Add inline comments for non-obvious logic
    - Explain marker stack operations, pipe delimiter handling, etc.
    - _Requirements: 9.3_
  
  - [x] 11.4 Format code according to PEP 8
    - Run formatter (black or autopep8) on all Python files
    - _Requirements: 9.5_

- [ ] 12. Add property-based tests
  - [ ]* 12.1 Write property test for tokenization completeness
    - **Property 1: Tokenization Completeness**
    - **Validates: Requirements 1.1, 1.3, 10.4**
    - Generate random USFM-like text, verify all tokens have valid types and content is preserved
  
  - [ ]* 12.2 Write property test for embedded marker splitting
    - **Property 2: Embedded Marker Splitting**
    - **Validates: Requirements 1.4**
    - Generate words with embedded markers, verify correct token sequence
  
  - [ ]* 12.3 Write property test for line number accuracy
    - **Property 3: Line Number Accuracy**
    - **Validates: Requirements 1.5**
    - Generate multi-line USFM text, verify token line numbers match source positions
  
  - [ ]* 12.4 Write property test for AST node type validity
    - **Property 4: AST Node Type Validity**
    - **Validates: Requirements 2.1**
    - Generate valid USFM structures, verify all AST nodes have valid types
  
  - [ ]* 12.5 Write property test for glossary pipe delimiter handling
    - **Property 5: Glossary Pipe Delimiter Handling**
    - **Validates: Requirements 2.3**
    - Generate glossary words with and without pipes, verify only text before pipe is preserved
  
  - [ ]* 12.6 Write property test for Accordance verse format
    - **Property 6: Accordance Verse Format**
    - **Validates: Requirements 4.1**
    - Generate verse nodes, verify output matches "BookName Chapter:Verse" pattern
  
  - [ ]* 12.7 Write property test for paragraph marker conditional rendering
    - **Property 7: Paragraph Marker Conditional Rendering**
    - **Validates: Requirements 4.2**
    - Generate verses with paragraph markers, verify ¶ appears when para=True and not when para=False
  
  - [ ]* 12.8 Write property test for text-critical mark suppression
    - **Property 8: Text-Critical Mark Suppression**
    - **Validates: Requirements 4.3**
    - Generate text with ⸂ and ⸃, verify marks are omitted when tc=False and included when tc=True
  
  - [ ]* 12.9 Write property test for footnote and cross-reference filtering
    - **Property 9: Footnote and Cross-Reference Filtering**
    - **Validates: Requirements 4.4**
    - Generate AST with Footnote and CrossRef nodes, verify content is not in output
  
  - [ ]* 12.10 Write property test for glossary word rendering
    - **Property 10: Glossary Word Rendering**
    - **Validates: Requirements 4.5**
    - Generate GlossaryWord nodes, verify only word portion is emitted
  
  - [ ]* 12.11 Write property test for skipped book filtering
    - **Property 11: Skipped Book Filtering**
    - **Validates: Requirements 4.6**
    - Generate books with skipped book IDs, verify empty output
  
  - [ ]* 12.12 Write property test for punctuation spacing
    - **Property 12: Punctuation Spacing**
    - **Validates: Requirements 4.7**
    - Generate text nodes with punctuation, verify no space before punctuation
  
  - [ ]* 12.13 Write property test for BOM handling
    - **Property 13: BOM Handling**
    - **Validates: Requirements 6.1**
    - Generate files with UTF-8 BOM, verify BOM doesn't appear in AST
  
  - [ ]* 12.14 Write property test for line ending normalization
    - **Property 14: Line Ending Normalization**
    - **Validates: Requirements 6.2**
    - Generate files with \r\n line endings, verify normalization to \n
  
  - [ ]* 12.15 Write property test for Unicode preservation
    - **Property 15: Unicode Preservation**
    - **Validates: Requirements 6.3**
    - Generate USFM with Unicode characters, verify preservation through parse and render
  
  - [ ]* 12.16 Write property test for error message context
    - **Property 16: Error Message Context**
    - **Validates: Requirements 10.1**
    - Generate parsing errors, verify exception includes filename and line number
  
  - [ ]* 12.17 Write property test for unknown marker warning
    - **Property 17: Unknown Marker Warning and Continuation**
    - **Validates: Requirements 10.2**
    - Generate USFM with unknown markers, verify warning to stderr and continued processing
  
  - [ ]* 12.18 Write property test for structural error detection
    - **Property 18: Structural Error Detection**
    - **Validates: Requirements 10.3**
    - Generate USFM missing chapter/verse numbers, verify descriptive exception
  
  - [ ]* 12.19 Write property test for round-trip AST preservation
    - **Property 19: Round-Trip AST Preservation**
    - **Validates: Requirements 11.2**
    - Generate valid USFM, verify parse → render → parse produces equivalent AST
  
  - [ ]* 12.20 Write property test for marker recognition completeness
    - **Property 20: Marker Recognition Completeness**
    - **Validates: Requirements 12.1-12.13**
    - Generate USFM with all supported markers, verify all are recognized correctly

- [x] 13. Create documentation and examples
  - [x] 13.1 Create README.md with usage examples
    - Document CLI usage with examples
    - Document programmatic usage (importing modules)
    - Include examples for each walker type
    - _Requirements: 7.1, 7.2, 7.3_
  
  - [x] 13.2 Create example scripts
    - Create example script showing SimplifyWalker usage
    - Create example script showing paragraph extract/apply workflow
    - _Requirements: 11.3, 11.4_

- [x] 14. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- The implementation follows the migration path outlined in the design: lexer → parser → AccordanceWalker → test compatibility → SimplifyWalker → paragraph walkers → property tests → documentation
- Python 3.7+ is required for dataclasses
- The click library is acceptable as the only external dependency for CLI
- Testing uses pytest for all unit, integration, and property-based tests
- Backward compatibility is verified through pytest integration tests comparing against reference .acc files
