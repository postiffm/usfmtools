# USFM Parser Examples

This directory contains example scripts demonstrating how to use the USFM parser tools programmatically.

## Examples

### example_simplify.py

Demonstrates using `SimplifyWalker` to convert USFM files to plain text without verse references or markers. Useful for AI training data or text analysis.

**Usage:**
```bash
python example_simplify.py input.usfm > output.txt
```

**What it does:**
- Parses a USFM file
- Removes all verse references and markers
- Outputs clean running text

### example_paragraphs.py

Demonstrates the paragraph extract/apply workflow for transferring paragraph formatting between files.

**Usage:**
```bash
# Extract paragraph markers from a file
python example_paragraphs.py extract input.usfm paragraphs.txt

# Show paragraph locations
python example_paragraphs.py show input.usfm

# Apply paragraph markers to another file
python example_paragraphs.py apply input.usfm paragraphs.txt output.acc
```

**What it does:**
- Extracts paragraph marker locations from USFM files
- Saves paragraph maps to text files
- Applies paragraph markers to other USFM files
- Displays paragraph locations

## Running the Examples

Make sure you have the `usfmtools` package in your Python path. The examples automatically add the parent directory to the path, so you can run them directly from the examples directory:

```bash
cd examples
python example_simplify.py ../test1.usfm
python example_paragraphs.py show ../test1.usfm
```

## Creating Your Own Scripts

Use these examples as templates for your own USFM processing scripts. The key pattern is:

1. Import the necessary modules from `usfmtools`
2. Create a `UsfmParser` instance
3. Parse your USFM file with `parser.load()` or `parser.loads()`
4. Create a walker instance (AccordanceWalker, SimplifyWalker, or custom)
5. Render the output with `walker.render(document)`

See the main README.md for more details on the API.
