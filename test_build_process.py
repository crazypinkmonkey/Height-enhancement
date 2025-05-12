"""
Tests for the documentation build process.

This module contains tests to verify that the documentation can be built
correctly and that all build artifacts are generated as expected.
"""

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

# Import test configuration
from .test_config import DOCS_DIR, PROJECT_ROOT

# Skip these tests if we're not in a development environment
pytestmark = pytest.mark.skipif(
    not os.environ.get("TEST_DOCS"),
    reason="Set TEST_DOCS=1 to run documentation tests"
)

class TestBuildProcess:
    """Tests for the documentation build process."""
    
    @pytest.fixture(scope="class")
    def build_dir(self):
        """Create a temporary build directory for tests."""
        with tempfile.TemporaryDirectory(prefix="height_docs_build_") as tmpdir:
            yield Path(tmpdir)
    
    def test_sphinx_build(self, build_dir):
        """Test that the documentation can be built with Sphinx."""
        # Build the documentation
        cmd = [
            "sphinx-build",
            "-b", "html",
            "-d", str(build_dir / "doctrees"),
            str(DOCS_DIR),
            str(build_dir / "html")
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check for build errors
        assert result.returncode == 0, f"Build failed with errors:\n{result.stderr}"
        
        # Check for build warnings
        warning_patterns = [
            r'warning',
            r'error',
            r'failed',
            r'traceback',
            r'exception',
        ]
        
        for pattern in warning_patterns:
            assert not re.search(pattern, result.stderr, re.IGNORECASE), \
                f"Build warnings or errors found in output: {result.stderr}"
        
        # Check that the index file was created
        index_file = build_dir / "html" / "index.html"
        assert index_file.exists(), f"Index file not found: {index_file}"
    
    def test_build_output(self, build_dir):
        """Test that the build output contains all expected files."""
        # Build the documentation
        cmd = [
            "sphinx-build",
            "-b", "html",
            "-d", str(build_dir / "doctrees"),
            str(DOCS_DIR),
            str(build_dir / "html")
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Build failed with errors:\n{result.stderr}"
        
        # Check for expected files in the build output
        expected_files = [
            "index.html",
            "_static/theme.css",
            "_static/theme.js",
            "genindex.html",
            "search.html",
            "searchindex.js",
        ]
        
        for file_name in expected_files:
            file_path = build_dir / "html" / file_name
            assert file_path.exists(), f"Expected file not found in build output: {file_path}"
    
    def test_build_warnings(self, build_dir):
        """Test that the documentation builds without warnings."""
        # Build the documentation with warnings as errors
        cmd = [
            "sphinx-build",
            "-W",  # Turn warnings into errors
            "-b", "html",
            "-d", str(build_dir / "doctrees"),
            str(DOCS_DIR),
            str(build_dir / "html")
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check for build errors
        assert result.returncode == 0, f"Build failed with warnings:\n{result.stderr}"
    
    @pytest.mark.parametrize("builder", ["html", "latex", "man", "texinfo"])
    def test_builders(self, build_dir, builder):
        """Test that the documentation can be built with different builders."""
        # Skip builders that require additional dependencies
        if builder in ["latex", "man", "texinfo"]:
            pytest.skip(f"{builder} builder requires additional dependencies")
        
        # Build the documentation
        cmd = [
            "sphinx-build",
            "-b", builder,
            "-d", str(build_dir / "doctrees"),
            str(DOCS_DIR),
            str(build_dir / builder)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check for build errors
        assert result.returncode == 0, f"Build with {builder} builder failed:\n{result.stderr}"
        
        # Check that the output directory was created
        output_dir = build_dir / builder
        assert output_dir.exists(), f"Output directory not found: {output_dir}"
        
        # Check that the output directory is not empty
        assert any(output_dir.iterdir()), f"Output directory is empty: {output_dir}"

class TestCleanBuild:
    """Tests for cleaning the build directory."""
    
    def test_clean(self, build_dir):
        """Test that the build directory can be cleaned."""
        # Build the documentation
        cmd = [
            "sphinx-build",
            "-b", "html",
            "-d", str(build_dir / "doctrees"),
            str(DOCS_DIR),
            str(build_dir / "html")
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Build failed with errors:\n{result.stderr}"
        
        # Clean the build directory
        cmd = [
            "sphinx-build",
            "-M", "clean",
            str(DOCS_DIR),
            str(build_dir)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Clean failed with errors:\n{result.stderr}"
        
        # Check that the build directory is empty
        assert not any(build_dir.iterdir()), f"Build directory is not empty: {build_dir}"

if __name__ == "__main__":
    pytest.main([__file__])
