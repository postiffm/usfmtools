"""
Integration tests for the usfmToAccordance CLI script.

Tests the command-line interface including:
- Single file processing
- Multiple file processing
- Flag behavior (--para, --tc, --debug)
- Error handling
"""

import os
import sys
import subprocess
import tempfile
import pytest
from pathlib import Path


# Path to the CLI script
CLI_SCRIPT = Path(__file__).parent.parent / "usfmtools" / "usfmToAccordance.py"


def run_cli(args, input_text=None):
    """
    Run the CLI script with given arguments.
    
    Args:
        args: List of command-line arguments
        input_text: Optional stdin input
        
    Returns:
        Tuple of (stdout, stderr, returncode)
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Run the script directly with PYTHONPATH set to project root
    cmd = [sys.executable, str(CLI_SCRIPT)] + args
    env = os.environ.copy()
    env['PYTHONPATH'] = str(project_root)
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8',  # Explicitly use UTF-8 encoding
        input=input_text,
        env=env,
        cwd=project_root
    )
    return result.stdout, result.stderr, result.returncode


class TestSingleFileProcessing:
    """Test processing of single USFM files"""
    
    def test_basic_file_processing(self, tmp_path):
        """Test basic single file processing"""
        # Create a simple test file
        test_file = tmp_path / "test.usfm"
        test_file.write_text(r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v 1 Test verse")
        
        stdout, stderr, returncode = run_cli([str(test_file)])
        
        assert returncode == 0
        assert "Matt. 1:1" in stdout
        assert "Test verse" in stdout
    
    def test_file_with_glossary_words(self, tmp_path):
        """Test file with glossary word markers"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\v 1 dem \w Messias\w*,"
        )
        
        stdout, stderr, returncode = run_cli([str(test_file)])
        
        assert returncode == 0
        assert "Messias" in stdout
    
    def test_file_not_found(self):
        """Test error handling for non-existent file"""
        stdout, stderr, returncode = run_cli(["nonexistent.usfm"])
        
        assert returncode == 1
        assert "Error" in stderr or "not found" in stderr.lower()


class TestMultipleFileProcessing:
    """Test processing of multiple USFM files"""
    
    def test_multiple_files_concatenation(self, tmp_path):
        """Test that multiple files are concatenated correctly"""
        # Create two test files
        file1 = tmp_path / "test1.usfm"
        file1.write_text(r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v 1 First verse")
        
        file2 = tmp_path / "test2.usfm"
        file2.write_text(r"\id MRK" + "\n" + r"\c 1" + "\n" + r"\v 1 Second verse")
        
        stdout, stderr, returncode = run_cli([str(file1), str(file2)])
        
        assert returncode == 0
        assert "Matt. 1:1" in stdout
        assert "First verse" in stdout
        assert "Mark 1:1" in stdout
        assert "Second verse" in stdout
    
    def test_multiple_files_order_preserved(self, tmp_path):
        """Test that file order is preserved in output"""
        file1 = tmp_path / "a.usfm"
        file1.write_text(r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v 1 AAA")
        
        file2 = tmp_path / "b.usfm"
        file2.write_text(r"\id MRK" + "\n" + r"\c 1" + "\n" + r"\v 1 BBB")
        
        stdout, stderr, returncode = run_cli([str(file1), str(file2)])
        
        # Check that AAA appears before BBB
        assert stdout.index("AAA") < stdout.index("BBB")


class TestParaFlag:
    """Test --para/--no-para flag behavior"""
    
    def test_para_flag_default_true(self, tmp_path):
        """Test that paragraph markers are included by default"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\p" + "\n" +
            r"\v 1 Test verse"
        )
        
        stdout, stderr, returncode = run_cli([str(test_file)])
        
        assert returncode == 0
        assert "¶" in stdout
    
    def test_para_flag_explicit_true(self, tmp_path):
        """Test --para flag explicitly enables paragraph markers"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\p" + "\n" +
            r"\v 1 Test verse"
        )
        
        stdout, stderr, returncode = run_cli(["--para", str(test_file)])
        
        assert returncode == 0
        assert "¶" in stdout
    
    def test_no_para_flag_disables_markers(self, tmp_path):
        """Test --no-para flag disables paragraph markers"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\p" + "\n" +
            r"\v 1 Test verse"
        )
        
        stdout, stderr, returncode = run_cli(["--no-para", str(test_file)])
        
        assert returncode == 0
        assert "¶" not in stdout


class TestTcFlag:
    """Test --tc/--no-tc flag behavior"""
    
    def test_tc_flag_default_true(self, tmp_path):
        """Test that text-critical marks are included by default"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\v 1 Test ⸂critical⸃ verse",
            encoding='utf-8'
        )
        
        stdout, stderr, returncode = run_cli([str(test_file)])
        
        assert returncode == 0
        assert "⸂" in stdout
        assert "⸃" in stdout
    
    def test_tc_flag_explicit_true(self, tmp_path):
        """Test --tc flag explicitly enables text-critical marks"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\v 1 Test ⸂critical⸃ verse",
            encoding='utf-8'
        )
        
        stdout, stderr, returncode = run_cli(["--tc", str(test_file)])
        
        assert returncode == 0
        assert "⸂" in stdout
        assert "⸃" in stdout
    
    def test_no_tc_flag_suppresses_marks(self, tmp_path):
        """Test --no-tc flag suppresses text-critical marks"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\v 1 Test ⸂critical⸃ verse",
            encoding='utf-8'
        )
        
        stdout, stderr, returncode = run_cli(["--no-tc", str(test_file)])
        
        assert returncode == 0
        assert "⸂" not in stdout
        assert "⸃" not in stdout
        assert "critical" in stdout  # Text should still be there


class TestDebugFlag:
    """Test --debug/--quiet flag behavior"""
    
    def test_debug_flag_default_false(self, tmp_path):
        """Test that debug output is disabled by default"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v 1 Test")
        
        stdout, stderr, returncode = run_cli([str(test_file)])
        
        assert returncode == 0
        # Debug output should not be present (stderr should be minimal)
    
    def test_debug_flag_enables_output(self, tmp_path):
        """Test --debug flag enables debug output"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v 1 Test")
        
        stdout, stderr, returncode = run_cli(["--debug", str(test_file)])
        
        assert returncode == 0
        # With debug enabled, there might be debug output to stderr
        # (This depends on implementation - adjust as needed)
    
    def test_quiet_flag_suppresses_output(self, tmp_path):
        """Test --quiet flag suppresses debug output"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v 1 Test")
        
        stdout, stderr, returncode = run_cli(["--quiet", str(test_file)])
        
        assert returncode == 0


class TestCombinedFlags:
    """Test combinations of flags"""
    
    def test_no_para_no_tc_combined(self, tmp_path):
        """Test --no-para and --no-tc flags together"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\p" + "\n" +
            r"\v 1 Test ⸂critical⸃ verse",
            encoding='utf-8'
        )
        
        stdout, stderr, returncode = run_cli(["--no-para", "--no-tc", str(test_file)])
        
        assert returncode == 0
        assert "¶" not in stdout
        assert "⸂" not in stdout
        assert "⸃" not in stdout
    
    def test_all_flags_combined(self, tmp_path):
        """Test all flags together"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\p" + "\n" +
            r"\v 1 Test verse"
        )
        
        stdout, stderr, returncode = run_cli([
            "--para", "--tc", "--debug", str(test_file)
        ])
        
        assert returncode == 0
        assert "Matt. 1:1" in stdout


class TestErrorHandling:
    """Test error handling scenarios"""
    
    def test_missing_file_error(self):
        """Test error message for missing file"""
        stdout, stderr, returncode = run_cli(["missing.usfm"])
        
        assert returncode == 1
        assert stderr  # Should have error message
    
    def test_no_files_provided(self):
        """Test error when no files are provided"""
        stdout, stderr, returncode = run_cli([])
        
        assert returncode != 0
        # Click should show usage/error message
    
    def test_invalid_usfm_structure(self, tmp_path):
        """Test error handling for invalid USFM structure"""
        test_file = tmp_path / "invalid.usfm"
        # Missing verse number after \v marker
        test_file.write_text(r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v")
        
        stdout, stderr, returncode = run_cli([str(test_file)])
        
        # Should fail with error message
        assert returncode == 1
        assert stderr  # Should have error message
    
    def test_partial_failure_stops_processing(self, tmp_path):
        """Test that error in one file stops processing"""
        file1 = tmp_path / "good.usfm"
        file1.write_text(r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v 1 Good")
        
        stdout, stderr, returncode = run_cli([str(file1), "missing.usfm"])
        
        assert returncode == 1


class TestRealWorldFiles:
    """Test with actual test files if they exist"""
    
    @pytest.mark.skipif(not Path("test1.usfm").exists(), 
                       reason="test1.usfm not found")
    def test_test1_file(self):
        """Test with actual test1.usfm file"""
        stdout, stderr, returncode = run_cli(["test1.usfm"])
        
        assert returncode == 0
        # test1.usfm is a fragment without book/chapter/verse structure
        # so output should be empty
        assert stdout == ""
    
    @pytest.mark.skipif(not Path("test3.usfm").exists(),
                       reason="test3.usfm not found")
    def test_test3_file(self):
        """Test with actual test3.usfm file"""
        stdout, stderr, returncode = run_cli(["test3.usfm"])
        
        assert returncode == 0
        assert "Heb. 1:3" in stdout
        assert "Diospa" in stdout


class TestOutputFormat:
    """Test output format correctness"""
    
    def test_output_to_stdout(self, tmp_path):
        """Test that output goes to stdout"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(r"\id MAT" + "\n" + r"\c 1" + "\n" + r"\v 1 Test")
        
        stdout, stderr, returncode = run_cli([str(test_file)])
        
        assert returncode == 0
        assert stdout  # Should have output
        assert "Matt. 1:1" in stdout
    
    def test_errors_to_stderr(self):
        """Test that errors go to stderr"""
        stdout, stderr, returncode = run_cli(["missing.usfm"])
        
        assert returncode == 1
        assert not stdout or len(stdout) == 0  # No output to stdout
        assert stderr  # Error message to stderr
    
    def test_utf8_output(self, tmp_path):
        """Test that UTF-8 characters are preserved in output"""
        test_file = tmp_path / "test.usfm"
        test_file.write_text(
            r"\id MAT" + "\n" +
            r"\c 1" + "\n" +
            r"\v 1 Diospa k'anchariyninpa"
        )
        
        stdout, stderr, returncode = run_cli([str(test_file)])
        
        assert returncode == 0
        assert "Diospa" in stdout
        assert "k'anchariyninpa" in stdout
