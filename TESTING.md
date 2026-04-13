# Testing the New USFM Parser

This document explains how to test the new modular USFM parser implementation.

## Overview

The new parser has been refactored from a monolithic implementation into a clean three-stage architecture:
- **Lexer** (`usfmtools/usfmlexer.py`) - Tokenizes USFM text
- **Parser** (`usfmtools/usfmparser.py`) - Builds an Abstract Syntax Tree (AST)
- **Walker** (`usfmtools/usfmwalker.py`) - Traverses the AST to generate output

The implementation is validated by a comprehensive pytest test suite with 136 tests covering all functionality.

## Prerequisites

```bash
# Python 3.7+ required
python3 --version

# Install dependencies
pip install click pytest
```

## Test Suite Structure

The test suite consists of 136 tests organized into multiple test modules:

### Unit Tests (118 tests)

**Lexer Tests** (`tests/test_lexer.py`) - 58 tests
- Token generation (markers, text, end markers)
- Embedded marker splitting (e.g., `word\w*`)
- Unknown marker warnings
- Line number tracking
- Edge cases and Unicode handling

**Parser Tests** (`tests/test_parser.py`) - 36 tests
- AST construction for all node types
- Glossary word pipe delimiter handling (`word|lemma`)
- Nested marker handling (footnotes, cross-references)
- Error detection (missing chapter/verse numbers)
- File encoding (UTF-8 BOM, CRLF normalization)

**Walker Tests** (`tests/test_walker.py`) - 24 tests
- Verse format (`BookName Chapter:Verse`)
- Paragraph marker insertion (¶)
- Text-critical mark suppression (⸂ and ⸃)
- Footnote and cross-reference filtering
- Punctuation spacing rules
- Skipped book filtering
- Glossary word rendering

### Integration Tests (18 tests)

**Integration Suite** (`tests/test_integration_suite.py`) - 18 tests
- 12 core tests validating against reference files (test1-test12)
- 2 CLI flag tests (para, tc)
- 2 encoding tests (BOM, CRLF)
- 2 error message tests

| Test | Input File | Expected Output | Description |
|------|------------|-----------------|-------------|
| 1 | test1.usfm | test1.acc | Glossary word with pipe delimiter |
| 2 | test2.usfm | test2.acc | Cross-references and poetry markers |
| 3 | test3.usfm | test3.acc | Basic verse |
| 4 | test4.usfm | test4.acc | Multiple USFM features |
| 5 | test5.usfm | (error) | Error test: missing verse number |
| 6 | test6.usfm | (error) | Error test: structural validation |
| 7 | test7.usfm | test7.acc | Additional features |
| 8 | test8.usfm | test8.acc | Additional features |
| 9 | test9.usfm | test9.acc | Additional features |
| 10 | test10.usfm | test10.acc | Additional features |
| 11 | test11.usfm | test11.acc | Additional features |
| 12 | test12.usfm | test12.acc | Additional features |

## Running the Tests

### Run All Tests

```bash
# Run complete test suite (136 tests)
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=usfmtools --cov-report=html

# Run with summary only
python -m pytest tests/
```

**Expected output:**
```
============================= test session starts =============================
...
======================== 136 passed in 2.06s =========================
```

### Run Specific Test Modules

```bash
# Run only lexer tests
python -m pytest tests/test_lexer.py -v

# Run only parser tests
python -m pytest tests/test_parser.py -v

# Run only walker tests
python -m pytest tests/test_walker.py -v

# Run only integration tests
python -m pytest tests/test_integration_suite.py -v

# Run only CLI tests
python -m pytest tests/test_cli.py -v
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
python -m pytest tests/test_integration_suite.py::TestIntegrationSuite -v

# Run a specific test function
python -m pytest tests/test_integration_suite.py::TestIntegrationSuite::test_test1_glossary_word -v

# Run tests matching a pattern
python -m pytest tests/ -k "glossary" -v
```

### Run with Different Output Formats

```bash
# Verbose output with test names
python -m pytest tests/ -v

# Show local variables on failure
python -m pytest tests/ -l

# Stop on first failure
python -m pytest tests/ -x

# Show print statements
python -m pytest tests/ -s

# Quiet mode (minimal output)
python -m pytest tests/ -q
```

## Understanding Test Results

### All Tests Pass
```
======================== 136 passed in 2.06s =========================
```
All tests pass successfully.

### Some Tests Fail
```
======================== 6 failed, 130 passed in 2.06s =========================
FAILED tests/test_cli.py::TestTcFlag::test_tc_flag_default_true
```
Shows which specific tests failed. Use `-v` flag for more details.

### Detailed Failure Information
```bash
python -m pytest tests/ -v --tb=short
```
Shows detailed traceback and assertion information for failures.

### Test a Specific Failing Test
```bash
python -m pytest tests/test_cli.py::TestTcFlag::test_tc_flag_default_true -vv
```
Runs only the failing test with maximum verbosity.

## CLI Usage

The CLI script is located in the usfmtools package:

```bash
# Basic usage
python usfmtools/usfmToAccordance.py test1.usfm > output.acc

# Multiple files
python usfmtools/usfmToAccordance.py test1.usfm test2.usfm test3.usfm > combined.acc

# Disable paragraph markers
python usfmtools/usfmToAccordance.py --no-para test1.usfm > output.acc

# Disable text-critical marks
python usfmtools/usfmToAccordance.py --no-tc test1.usfm > output.acc

# Enable debug output
python usfmtools/usfmToAccordance.py --debug test1.usfm > output.acc

# Show help
python usfmtools/usfmToAccordance.py --help
```

## Manual Testing

You can also test individual files manually:

```bash
# Test a single file
python usfmtools/usfmToAccordance.py test1.usfm > test1_output.acc

# Compare with expected output (Unix/Linux)
diff test1.acc test1_output.acc

# Compare with expected output (Windows PowerShell)
Compare-Object (Get-Content test1.acc) (Get-Content test1_output.acc)
```

## Common Issues and Solutions

### Issue: "ModuleNotFoundError: No module named 'click'"
**Solution:** Install the click library:
```bash
pip install click
```

### Issue: "ModuleNotFoundError: No module named 'pytest'"
**Solution:** Install pytest:
```bash
pip install pytest
```

### Issue: "UnicodeEncodeError" on Windows
**Solution:** The implementation automatically handles UTF-8 encoding. Ensure you're using Python 3.7+:
```bash
python3 --version
```

### Issue: Tests fail with import errors
**Solution:** Ensure you're running pytest from the workspace root directory:
```bash
cd /path/to/usfmtools
python -m pytest tests/
```

### Issue: Specific test fails
**Solution:** Run the test with verbose output to see detailed error information:
```bash
python -m pytest tests/test_name.py::TestClass::test_function -vv
```

## Test Coverage

The test suite validates:

✓ **Lexer functionality:**
- Token generation (markers, text, end markers)
- Embedded marker splitting (e.g., `word\w*`)
- Unknown marker warnings
- Line number tracking

✓ **Parser functionality:**
- AST construction for all node types
- Glossary word pipe delimiter handling (`word|lemma`)
- Nested marker handling (footnotes, cross-references)
- Error detection (missing chapter/verse numbers)
- UTF-8 and Unicode support

✓ **Walker functionality:**
- Verse format (`BookName Chapter:Verse`)
- Paragraph marker insertion (¶)
- Text-critical mark suppression (⸂ and ⸃)
- Footnote and cross-reference filtering
- Punctuation spacing rules
- Skipped book filtering
- Glossary word rendering

✓ **CLI functionality:**
- Multiple file processing
- Flag handling (--para, --tc, --debug)
- Error handling and reporting
- UTF-8 output encoding

## Next Steps

After running the test suite:

1. **Fix failing tests:** Address any test failures before proceeding
2. **Run with real data:** Test with complete Bible files (e.g., `41MATLTZ.SFM`)
3. **Implement remaining features:** SimplifyWalker, ParagraphExtractWalker, etc.
4. **Add property-based tests:** Validate universal correctness properties using Hypothesis
5. **Create documentation:** API docs and usage examples

## Troubleshooting

If tests fail unexpectedly:

1. **Check Python version:** Requires Python 3.7+ for dataclasses
   ```bash
   python3 --version
   ```

2. **Verify dependencies are installed:**
   ```bash
   pip list | grep -E "(click|pytest)"
   ```

3. **Check for file modifications:** Ensure test files haven't been modified
   ```bash
   git status test*.usfm test*.acc
   ```

4. **Run with maximum verbosity:**
   ```bash
   python -m pytest tests/ -vv --tb=long
   ```

5. **Run a single test to isolate issues:**
   ```bash
   python -m pytest tests/test_integration_suite.py::TestIntegrationSuite::test_test1_glossary_word -vv
   ```

## Reference

For more information about the implementation:
- **Design document:** `.kiro/specs/usfm-parser-refactor/design.md`
- **Requirements document:** `.kiro/specs/usfm-parser-refactor/requirements.md`
- **Implementation tasks:** `.kiro/specs/usfm-parser-refactor/tasks.md`

## Test File Locations

- **Unit tests:** `tests/test_lexer.py`, `tests/test_parser.py`, `tests/test_walker.py`, `tests/test_cli.py`
- **Integration tests:** `tests/test_integration_suite.py`
- **Test data:** `test1.usfm` through `test12.usfm` and corresponding `.acc` files in workspace root

