"""
Tests for documentation configuration.

This module contains tests to verify that the documentation configuration
is correct and all settings are applied as expected.
"""

import os
import re
import sys
from pathlib import Path

import pytest

# Import test configuration
from .test_config import DOCS_DIR, PROJECT_ROOT, EXPECTED_EXTENSIONS, EXPECTED_CONFIG

# Skip these tests if we're not in a development environment
pytestmark = pytest.mark.skipif(
    not os.environ.get("TEST_DOCS"),
    reason="Set TEST_DOCS=1 to run documentation tests"
)

class TestConfiguration:
    """Tests for documentation configuration."""
    
    def test_conf_py_exists(self):
        """Test that conf.py exists."""
        conf_py = DOCS_DIR / "conf.py"
        assert conf_py.exists(), f"Configuration file not found: {conf_py}"
    
    def test_conf_py_contents(self):
        """Test that conf.py contains the expected settings."""
        conf_py = DOCS_DIR / "conf.py"
        assert conf_py.exists(), f"Configuration file not found: {conf_py}"
        
        # Read the configuration file
        content = conf_py.read_text(encoding='utf-8')
        
        # Check for required settings
        required_settings = [
            r'project\s*=',
            r'author\s*=',
            r'release\s*=',
            r'extensions\s*=',
            r'html_theme\s*=',
            r'html_static_path\s*=',
            r'html_css_files\s*=',
            r'html_js_files\s*=',
        ]
        
        for setting in required_settings:
            assert re.search(setting, content), f"Required setting not found in conf.py: {setting}"
    
    def test_extensions_loaded(self):
        """Test that all required Sphinx extensions are loaded."""
        conf_py = DOCS_DIR / "conf.py"
        assert conf_py.exists(), f"Configuration file not found: {conf_py}"
        
        # Read the configuration file
        content = conf_py.read_text(encoding='utf-8')
        
        # Extract the extensions list
        extensions_match = re.search(r'extensions\s*=\s*\[(.*?)\]', content, re.DOTALL)
        assert extensions_match, "Extensions list not found in conf.py"
        
        extensions_str = extensions_match.group(1)
        
        # Check that all expected extensions are present
        for extension in EXPECTED_EXTENSIONS:
            assert f"'{extension}'" in extensions_str or f'"{extension}"' in extensions_str, \
                f"Expected extension not found in conf.py: {extension}"
    
    def test_theme_configuration(self):
        """Test that the theme is configured correctly."""
        conf_py = DOCS_DIR / "conf.py"
        assert conf_py.exists(), f"Configuration file not found: {conf_py}"
        
        # Read the configuration file
        content = conf_py.read_text(encoding='utf-8')
        
        # Check that the theme is set correctly
        assert "html_theme = 'sphinx_rtd_theme'" in content or \
               'html_theme = "sphinx_rtd_theme"' in content, \
               "Theme not set correctly in conf.py"
    
    def test_static_files(self):
        """Test that static files are configured correctly."""
        conf_py = DOCS_DIR / "conf.py"
        assert conf_py.exists(), f"Configuration file not found: {conf_py}"
        
        # Read the configuration file
        content = conf_py.read_text(encoding='utf-8')
        
        # Check that static files are included
        assert "html_static_path = ['_static']" in content or \
               'html_static_path = ["_static"]' in content, \
               "Static files path not set correctly in conf.py"
        
        # Check that CSS and JS files are included
        assert "'theme.css'" in content or '\"theme.css\"' in content, \
               "Theme CSS file not included in conf.py"
        assert "'theme.js'" in content or '\"theme.js\"' in content, \
               "Theme JS file not included in conf.py"

class TestMakefile:
    """Tests for the Makefile."""
    
    def test_makefile_exists(self):
        """Test that the Makefile exists."""
        makefile = DOCS_DIR / "Makefile"
        assert makefile.exists(), f"Makefile not found: {makefile}"
    
    def test_makefile_contents(self):
        """Test that the Makefile contains the expected targets."""
        makefile = DOCS_DIR / "Makefile"
        assert makefile.exists(), f"Makefile not found: {makefile}"
        
        # Read the Makefile
        content = makefile.read_text(encoding='utf-8')
        
        # Check for required targets
        required_targets = [
            'help',
            'clean',
            'html',
            'dirhtml',
            'singlehtml',
            'pickle',
            'json',
            'htmlhelp',
            'qthelp',
            'devhelp',
            'epub',
            'latex',
            'latexpdf',
            'latexpdfja',
            'text',
            'man',
            'texinfo',
            'info',
            'gettext',
            'changes',
            'linkcheck',
            'doctest',
            'coverage',
            'xml',
            'pseudoxml',
        ]
        
        for target in required_targets:
            assert f'.PHONY: {target}' in content or f'.PHONY: {target} ' in content, \
                f"Required target not found in Makefile: {target}"

if __name__ == "__main__":
    pytest.main([__file__])
