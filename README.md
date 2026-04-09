# USFM Parser Tools

A clean, modular USFM (Unified Standard Format Markers) parser following a three-stage compiler architecture: Lexer → Parser → Walker. This toolkit processes Bible text files in USFM format and supports multiple output formats including Accordance import format and simplified plain text for AI training.

## Features

- **Modular Architecture**: Separate lexer, parser, and walker components for maintainability
- **Multiple Output Formats**: Accordance format, simplified text, and extensible walker pattern
- **Robust Error Handling**: Descriptive error messages with filename and line number context
- **Unicode Support**: Full Unicode preservation with BOM handling
- **Cross-Platform**: Works on Ubuntu, WSL2, and other Unix-like environments

## Installation

No external dependencies required beyond Python 3.7+ standard library (except `click` for CLI).

```bash
# Install click for CLI usage
pip install click

# Or use the modules programmatically without any dependencies
```

## Command-Line Usage

### Basic Usage

Convert USFM files to Accordance format:

```bash
python -m usfmtools.usfmToAccordance input.usfm > output.acc
```

### Multiple Files

Process multiple USFM files into a single output:

```bash
python -m usfmtools.usfmToAccordance book1.usfm book2.usfm book3.usfm > combined.acc
```

### Command-Line Options

```bash
# Disable paragraph markers (¶)
python -m usfmtools.usfmToAccordance --no-para input.usfm > output.acc

# Disable text-critical marks (⸂ and ⸃)
python -m usfmtools.usfmToAccordance --no-tc input.usfm > output.acc

# Enable debug output
python -m usfmtools.usfmToAccordance --debug input.usfm > output.acc

# Combine options
python -m usfmtools.usfmToAccordance --no-para --no-tc input.usfm > output.acc
```

## Programmatic Usage

### Basic Parsing

```python
from usfmtools.usfmparser import UsfmParser

# Parse a USFM file
parser = UsfmParser()
document = parser.load('input.usfm')

# Parse a USFM string
usfm_text = r"""
\id MAT
\c 1
\v 1 In the beginning...
"""
document = parser.loads(usfm_text)
```

### AccordanceWalker - Generate Accordance Format

```python
from usfmtools.usfmparser import UsfmParser
from usfmtools.usfmwalker import AccordanceWalker

# Parse and render to Accordance format
parser = UsfmParser()
document = parser.load('matthew.usfm')

walker = AccordanceWalker(para=True, tc=True)
output = walker.render(document)
print(output)

# Output format:
# Matt. 1:1 In the beginning...
# Matt. 1:2 ¶ And it came to pass...
```

### SimplifyWalker - Generate Plain Text

```python
from usfmtools.usfmparser import UsfmParser
from usfmtools.usfmwalker import SimplifyWalker

# Parse and render to simplified text (no verse references)
parser = UsfmParser()
document = parser.load('matthew.usfm')

walker = SimplifyWalker()
output = walker.render(document)
print(output)

# Output format:
# In the beginning... And it came to pass...
```

### ParagraphExtractWalker - Extract Paragraph Locations

```python
from usfmtools.usfmparser import UsfmParser
from usfmtools.usfmwalker import ParagraphExtractWalker

# Extract paragraph marker locations
parser = UsfmParser()
document = parser.load('matthew.usfm')

walker = ParagraphExtractWalker()
paragraph_map = walker.extract(document)

# paragraph_map is a dict: {"MAT 1:2": True, "MAT 2:1": True, ...}
for verse_ref in paragraph_map:
    print(f"Paragraph at {verse_ref}")
```

### ParagraphApplyWalker - Insert Paragraph Markers

```python
from usfmtools.usfmparser import UsfmParser
from usfmtools.usfmwalker import ParagraphApplyWalker, AccordanceWalker

# Apply paragraph markers from a map
parser = UsfmParser()
document = parser.load('matthew.usfm')

paragraph_map = {
    "MAT 1:2": True,
    "MAT 2:1": True,
}

walker = ParagraphApplyWalker(paragraph_map)
modified_document = walker.apply(document)

# Render with paragraph markers
output_walker = AccordanceWalker(para=True)
output = output_walker.render(modified_document)
```

### Lexer - Direct Tokenization

```python
from usfmtools.usfmlexer import tokenize

# Tokenize USFM text
usfm_text = r"\id MAT\c 1\v 1 In the beginning"
tokens = tokenize(usfm_text, filename='matthew.usfm')

for token in tokens:
    print(f"{token.type}: {token.value} (line {token.line})")

# Output:
# MARKER: id (line 1)
# TEXT: MAT (line 1)
# MARKER: c (line 1)
# TEXT: 1 (line 1)
# MARKER: v (line 1)
# TEXT: 1 (line 1)
# TEXT: In (line 1)
# TEXT: the (line 1)
# TEXT: beginning (line 1)
```

### Custom Walker - Create Your Own Output Format

```python
from usfmtools.usfmwalker import UsfmWalker
from usfmtools.usfmparser import UsfmParser

class MyCustomWalker(UsfmWalker):
    """Custom walker for your specific output format"""
    
    def __init__(self):
        self.verse_count = 0
    
    def visit_verse(self, node):
        self.verse_count += 1
        content = ''.join(self.render(child) for child in node.children)
        return f"[Verse {self.verse_count}] {content}\n"
    
    def visit_text(self, node):
        return node.value + " "

# Use your custom walker
parser = UsfmParser()
document = parser.load('matthew.usfm')

walker = MyCustomWalker()
output = walker.render(document)
print(output)
```

## Error Handling

The parser provides descriptive error messages with context:

```python
from usfmtools.usfmparser import UsfmParser

parser = UsfmParser()

try:
    document = parser.load('invalid.usfm')
except Exception as e:
    print(f"Parse error: {e}")
    # Output: Parse error: Missing verse number in invalid.usfm:15
```

Unknown markers generate warnings but don't stop processing:

```python
# USFM with unknown marker \xyz
# Output to stderr: Warning: Unknown marker '\xyz' at line 10
# Processing continues, content is preserved
```

## Architecture

The toolkit follows a three-stage compiler design:

1. **Lexer** (`usfmlexer.py`): Tokenizes raw USFM text into a stream of tokens
2. **Parser** (`usfmparser.py`): Converts tokens into an Abstract Syntax Tree (AST)
3. **Walker** (`usfmwalker.py`): Traverses the AST to generate output in various formats

This separation of concerns makes the code maintainable and extensible.

## Supported USFM Markers

- **Identification**: `\id`, `\rem`, `\h`, `\toc1`, `\toc2`, `\toc3`
- **Titles**: `\mt`, `\mt1`, `\mt2`, `\mt3`, `\ms`, `\imt1`, `\imt2`
- **Introductions**: `\is`, `\ip`, `\ipr`, `\imq`, `\iot`, `\io1`, `\io2`, `\io3`, `\ior`, `\ie`, `\ili`
- **Headings**: `\s`, `\s1`, `\s2`, `\s3`, `\r`, `\mr`, `\d`, `\qa`
- **Chapter/Verse**: `\c`, `\v`
- **Paragraphs**: `\p`, `\m`, `\mi`, `\nb`, `\b`, `\pi`, `\pi2`, `\pmo`
- **Poetry**: `\q`, `\q1`, `\q2`, `\q3`, `\q4`, `\qc`, `\qs`
- **Lists**: `\li`, `\li1`, `\li2`
- **Footnotes**: `\f`, `\fr`, `\fk`, `\ft`, `\fw`, `\fp`, `\f*`
- **Cross-references**: `\x`, `\xo`, `\xt`, `\x*`
- **Character styles**: `\w`, `\nd`, `\add`, `\qt`, `\tl`, `\rq`, `\k` (with end markers)
- **Tables**: `\tr`, `\th1`, `\th2`, `\th3`, `\tc1`, `\tc2`, `\tc3`
- **Special**: `\periph`, `\+w`

## Testing

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run specific test modules
pytest tests/test_lexer.py
pytest tests/test_parser.py
pytest tests/test_walker.py

# Run with verbose output
pytest -v

# Run integration tests
pytest tests/test_integration_suite.py
```

## Examples

See the `examples/` directory for complete working examples:

- `example_simplify.py`: Using SimplifyWalker for plain text output
- `example_paragraphs.py`: Extracting and applying paragraph markers

## Requirements

- Python 3.7+ (for dataclasses)
- `click` library (for CLI only, optional for programmatic usage)

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting pull requests.

## Documentation

For detailed design documentation, see `.kiro/specs/usfm-parser-refactor/design.md`.
