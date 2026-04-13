# Requirements Document

## Introduction

This document specifies requirements for refactoring the USFM parsing tools to eliminate spaghetti code and create reusable, maintainable components following a compiler design pattern. The system will parse USFM (Unified Standard Format Markers) files used for Bible text encoding and support multiple output formats including Accordance import format and simplified text for AI training.

## Glossary

- **USFM_Parser**: The system that tokenizes, parses, and transforms USFM files
- **Lexer**: The tokenization component that converts raw text into tokens
- **Parser**: The component that converts tokens into an Abstract Syntax Tree (AST)
- **Walker**: The component that traverses the AST to generate output
- **USFM_Marker**: A backslash-prefixed tag in USFM format (e.g., \p, \v, \c, \s1)
- **Accordance_Format**: The simplified .acc output format for Accordance Bible software
- **AST**: Abstract Syntax Tree representation of the parsed USFM document
- **End_Marker**: A closing USFM marker suffixed with asterisk (e.g., \w*, \f*)
- **Test_Suite**: The existing usfmToAccordanceTest.sh with test[1-n].acc reference outputs

## Requirements

### Requirement 1: Lexer Architecture

**User Story:** As a developer, I want a separate lexer component, so that I can easily add new USFM markers without modifying parser logic

#### Acceptance Criteria

1. THE Lexer SHALL tokenize USFM text into a sequence of tokens with types TOKEN_MARKER, TOKEN_MARKER_END, and TOKEN_TEXT
2. THE Lexer SHALL maintain a KNOWN_MARKERS set in a single location for all supported USFM markers
3. WHEN an unknown USFM marker is encountered, THE Lexer SHALL emit a TOKEN_MARKER with a warning to stderr and preserve the content
4. THE Lexer SHALL handle embedded markers within words (e.g., "justify\w*" becomes separate TEXT and MARKER_END tokens)
5. THE Lexer SHALL include line number information in each token for error reporting

### Requirement 2: Parser Architecture

**User Story:** As a developer, I want a separate parser component, so that I can create a tree representation suitable for multiple output formats

#### Acceptance Criteria

1. THE Parser SHALL convert token sequences into an Abstract Syntax Tree with node types for Document, Book, Chapter, Verse, Paragraph, Heading, Footnote, CrossRef, GlossaryWord, InlineSpan, Text, and Unknown
2. THE Parser SHALL track an open-marker stack to handle nested markers correctly
3. WHEN parsing glossary words with pipe delimiters, THE Parser SHALL extract the word before the pipe and discard the lemma form after the pipe
4. THE Parser SHALL provide a load() method that accepts a filename and returns a Document node
5. THE Parser SHALL provide a loads() method that accepts a text string and returns a Document node

### Requirement 3: Walker Architecture

**User Story:** As a developer, I want walker components that traverse the AST, so that I can generate different output formats from the same parsed structure

#### Acceptance Criteria

1. THE Walker SHALL provide a base UsfmWalker class with visit methods for each AST node type
2. THE Walker SHALL provide an AccordanceWalker subclass that generates .acc format output
3. THE Walker SHALL provide a SimplifyWalker subclass that generates plain text output without markers
4. THE Walker SHALL support configuration options passed to the constructor (e.g., para, tc flags)
5. THE Walker SHALL provide a render() method that accepts an AST node and returns a string

### Requirement 4: Accordance Output Format

**User Story:** As a Bible software user, I want to convert USFM files to Accordance format, so that I can import them into Accordance Bible software

#### Acceptance Criteria

1. WHEN generating Accordance output, THE AccordanceWalker SHALL format book headers as "BookName ChapterNum:VerseNum text..."
2. WHEN the para flag is True, THE AccordanceWalker SHALL insert " ¶" after verse references preceded by paragraph markers
3. WHEN the tc flag is False, THE AccordanceWalker SHALL suppress text-critical marks ⸂ and ⸃
4. THE AccordanceWalker SHALL discard footnote and cross-reference content
5. THE AccordanceWalker SHALL emit only the word portion of glossary entries (before the pipe delimiter)
6. THE AccordanceWalker SHALL skip books with codes: GLO, XXA, XXB, FRT, XXC, XXD, INT, BAK, XXE, XXF, XXG, CNC, TDX, OTH, TOB, JDT, ESG, WIS, SIR, BAR, 1MA, 2MA, 1ES, MAN, PS2, 3MA, 2ES, 4MA, DAG
7. THE AccordanceWalker SHALL apply punctuation spacing rules (no space before . , ; : ! ?)

### Requirement 5: Command-Line Interface

**User Story:** As a user, I want to run the parser from the command line with options, so that I can process USFM files in my workflow

#### Acceptance Criteria

1. THE USFM_Parser SHALL run from the command line in Ubuntu and WSL2 Windows environments
2. THE USFM_Parser SHALL accept a --para/--no-para flag with default True to control paragraph marker output
3. THE USFM_Parser SHALL accept a --tc/--no-tc flag with default True to control text-critical mark output
4. THE USFM_Parser SHALL accept a --debug/--quiet flag with default False to control debug output
5. THE USFM_Parser SHALL accept multiple input file arguments
6. WHEN processing multiple files, THE USFM_Parser SHALL concatenate output into a single stream

### Requirement 6: File Encoding and Line Endings

**User Story:** As a user working across platforms, I want the parser to handle different file encodings and line endings, so that I don't encounter cross-platform bugs

#### Acceptance Criteria

1. WHEN loading a file, THE Parser SHALL open files with utf-8-sig encoding to handle BOM transparently
2. WHEN loading a file, THE Parser SHALL normalize \r\n line endings to \n
3. THE Parser SHALL preserve all Unicode characters in the input text

### Requirement 7: Reusable Components

**User Story:** As a developer, I want to import parser components in other scripts, so that I can reuse USFM parsing logic for different utilities

#### Acceptance Criteria

1. THE Lexer SHALL be importable as a standalone module (usfmlexer.py)
2. THE Parser SHALL be importable as a standalone module (usfmparser.py)
3. THE Walker SHALL be importable as a standalone module (usfmwalker.py)
4. THE modules SHALL have no circular dependencies
5. THE modules SHALL have minimal external dependencies (no runtime dependencies beyond Python standard library)

### Requirement 8: Test Compatibility

**User Story:** As a maintainer, I want the refactored parser to pass existing tests, so that I can verify it produces correct output

#### Acceptance Criteria

1. WHEN processing test input files, THE USFM_Parser SHALL produce output matching the existing test[1-n].acc reference files
2. THE USFM_Parser SHALL support execution via the existing usfmToAccordanceTest.sh test script
3. THE USFM_Parser SHALL provide pytest-compatible unit tests in tests/test_usfm.py

### Requirement 9: Code Quality and Maintainability

**User Story:** As a maintainer, I want readable and documented code, so that I can understand and modify it quickly

#### Acceptance Criteria

1. THE USFM_Parser SHALL use clear, readable Python code without overly complex idioms
2. THE USFM_Parser SHALL include docstrings for all public classes and functions
3. THE USFM_Parser SHALL include inline comments explaining non-obvious logic
4. THE USFM_Parser SHALL use type hints for function parameters and return values
5. THE USFM_Parser SHALL follow PEP 8 style guidelines

### Requirement 10: Error Handling

**User Story:** As a user, I want clear error messages when parsing fails, so that I can identify and fix problems in USFM files

#### Acceptance Criteria

1. WHEN a parsing error occurs, THE Parser SHALL include the filename and line number in the error message
2. WHEN an unknown marker is encountered, THE Parser SHALL emit a warning to stderr but continue processing
3. WHEN a required structural element is missing (e.g., chapter number), THE Parser SHALL raise a descriptive exception
4. THE Parser SHALL preserve all text content even when encountering unknown markers

### Requirement 11: Extensibility for Future Formats

**User Story:** As a developer, I want the architecture to support future output formats, so that I can add USX export or other transformations

#### Acceptance Criteria

1. THE Walker architecture SHALL allow creation of new walker subclasses without modifying the Parser or Lexer
2. THE AST node structure SHALL preserve sufficient information to support round-trip transformations
3. THE Walker SHALL provide a ParagraphExtractWalker that returns a dictionary mapping verse references to paragraph markers
4. THE Walker SHALL provide a ParagraphApplyWalker that inserts paragraph markers at specified verse locations

### Requirement 12: Marker Coverage

**User Story:** As a user, I want support for commonly used USFM markers, so that I can process real-world Bible files

#### Acceptance Criteria

1. THE Lexer SHALL support identification markers: id, rem, h, toc1, toc2, toc3
2. THE Lexer SHALL support title markers: mt, mt1, mt2, mt3, ms, imt1, imt2
3. THE Lexer SHALL support introduction markers: is, ip, ipr, imq, iot, io1, io2, io3, ior, ie, ili
4. THE Lexer SHALL support heading markers: s, s1, s2, s3, r, mr, d, qa, ms
5. THE Lexer SHALL support chapter and verse markers: c, v
6. THE Lexer SHALL support paragraph markers: p, m, mi, nb, b, pi, pi2, pmo
7. THE Lexer SHALL support poetry markers: q, q1, q2, q3, q4, qc, qs
8. THE Lexer SHALL support list markers: li, li1, li2
9. THE Lexer SHALL support footnote markers: f, fr, fk, ft, fw, fp and end marker f*
10. THE Lexer SHALL support cross-reference markers: x, xo, xt and end marker x*
11. THE Lexer SHALL support character style markers: w, nd, add, qt, tl, rq, k and corresponding end markers
12. THE Lexer SHALL support table markers: tr, th1, th2, th3, tc1, tc2, tc3
13. THE Lexer SHALL support special markers: periph, +w
