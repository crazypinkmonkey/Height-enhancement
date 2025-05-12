"""
Tests for documentation content quality.

This module contains tests to verify that the documentation content
is complete, accurate, and follows the project's standards.
"""

import os
import re
import sys
from pathlib import Path

import pytest

# Import test configuration
from .test_config import DOCS_DIR, PROJECT_ROOT

# Skip these tests if we're not in a development environment
pytestmark = pytest.mark.skipif(
    not os.environ.get("TEST_DOCS"),
    reason="Set TEST_DOCS=1 to run documentation tests"
)

class TestContentQuality:
    """Tests for documentation content quality."""
    
    def test_readme_exists(self):
        """Test that README.md exists and is not empty."""
        readme = PROJECT_ROOT / "README.md"
        assert readme.exists(), f"README.md not found: {readme}"
        assert readme.stat().st_size > 0, f"README.md is empty: {readme}"
    
    def test_license_exists(self):
        """Test that LICENSE exists and is not empty."""
        license_file = PROJECT_ROOT / "LICENSE"
        assert license_file.exists(), f"LICENSE not found: {license_file}"
        assert license_file.stat().st_size > 0, f"LICENSE is empty: {license_file}"
    
    def test_contributing_exists(self):
        """Test that CONTRIBUTING.md exists and is not empty."""
        contributing = PROJECT_ROOT / "CONTRIBUTING.md"
        assert contributing.exists(), f"CONTRIBUTING.md not found: {contributing}"
        assert contributing.stat().st_size > 0, f"CONTRIBUTING.md is empty: {contributing}"
    
    def test_documentation_structure(self):
        """Test that the documentation has the expected structure."""
        # Check for required documentation files
        required_files = [
            "index.rst",
            "getting_started.rst",
            "installation.rst",
            "usage.rst",
            "api.rst",
            "examples.rst",
            "contributing.rst",
            "changelog.rst",
        ]
        
        for file_name in required_files:
            file_path = DOCS_DIR / file_name
            assert file_path.exists(), f"Required documentation file not found: {file_path}"
            assert file_path.stat().st_size > 0, f"Documentation file is empty: {file_path}"
    
    def test_rst_files(self):
        """Test that all .rst files are properly formatted."""
        for rst_file in DOCS_DIR.glob("**/*.rst"):
            # Skip files in _build directory
            if "_build" in str(rst_file):
                continue
                
            content = rst_file.read_text(encoding='utf-8')
            
            # Check for common RST formatting issues
            if rst_file.name != "changelog.rst":  # Changelog might have long lines
                for i, line in enumerate(content.split('\n'), 1):
                    assert len(line) <= 120, f"Line {i} in {rst_file} exceeds 120 characters"
            
            # Check for missing blank lines around code blocks
            code_block_pattern = re.compile(r'^::\\s*$|^\s*\S.*::\\s*$', re.MULTILINE)
            for match in code_block_pattern.finditer(content):
                line_num = content[:match.start()].count('\n') + 1
                line = match.group(0).strip()
                
                # Check for blank line before
                if line_num > 1 and content.split('\n')[line_num-2].strip() != '':
                    assert False, f"Missing blank line before code block at {rst_file}:{line_num}"
                
                # Check for blank line after
                if line_num < len(content.split('\n')) and content.split('\n')[line_num].strip() != '':
                    assert False, f"Missing blank line after code block at {rst_file}:{line_num}"
    
    def test_code_blocks_have_syntax_highlighting(self):
        """Test that all code blocks have syntax highlighting specified."""
        for rst_file in DOCS_DIR.glob("**/*.rst"):
            # Skip files in _build directory
            if "_build" in str(rst_file):
                continue
                
            content = rst_file.read_text(encoding='utf-8')
            
            # Find all code blocks
            code_blocks = re.findall(r'\n\s*::\\s*$|\n\s*\S.*::\\s*$', content, re.MULTILINE)
            
            for block in code_blocks:
                # Get the line number
                line_num = content[:content.find(block)].count('\n') + 1
                
                # Check if the code block has syntax highlighting
                if 'code-block::' not in content[content.find(block)-100:content.find(block)]:
                    assert False, f"Code block without syntax highlighting at {rst_file}:{line_num}"
    
    def test_no_broken_links(self, built_docs):
        """Test that there are no broken links in the documentation."""
        # This would test for broken internal and external links
        # In a real project, you would use a tool like linkcheck or Sphinx's built-in linkcheck builder
        pass
    
    def test_spelling(self, built_docs):
        """Test for spelling errors in the documentation."""
        # This would test for spelling errors in the documentation
        # In a real project, you would use a tool like sphinxcontrib.spelling or codespell
        pass

if __name__ == "__main__":
    pytest.main([__file__])
