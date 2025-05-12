"""
Tests for documentation static files.

This module contains tests to verify that all static files (CSS, JS, images, etc.)
are correctly included and functional in the documentation.
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

class TestStaticFiles:
    """Tests for static files."""
    
    def test_static_directory_exists(self):
        """Test that the static directory exists."""
        static_dir = DOCS_DIR / "_static"
        assert static_dir.exists(), f"Static directory not found: {static_dir}"
        assert static_dir.is_dir(), f"Static directory is not a directory: {static_dir}"
    
    def test_theme_css_exists(self):
        """Test that the theme CSS file exists."""
        css_file = DOCS_DIR / "_static" / "theme.css"
        assert css_file.exists(), f"Theme CSS file not found: {css_file}"
        assert css_file.is_file(), f"Theme CSS is not a file: {css_file}"
        
        # Check that the file is not empty
        assert css_file.stat().st_size > 0, f"Theme CSS file is empty: {css_file}"
    
    def test_theme_js_exists(self):
        """Test that the theme JavaScript file exists."""
        js_file = DOCS_DIR / "_static" / "theme.js"
        assert js_file.exists(), f"Theme JavaScript file not found: {js_file}"
        assert js_file.is_file(), f"Theme JavaScript is not a file: {js_file}"
        
        # Check that the file is not empty
        assert js_file.stat().st_size > 0, f"Theme JavaScript file is empty: {js_file}"
    
    def test_images_exist(self):
        """Test that all image files exist and are not empty."""
        image_dir = DOCS_DIR / "_static" / "images"
        if not image_dir.exists():
            pytest.skip(f"Images directory not found: {image_dir}")
        
        # Check all image files
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg', '*.ico']:
            for img_file in image_dir.glob(ext):
                assert img_file.is_file(), f"Image is not a file: {img_file}"
                assert img_file.stat().st_size > 0, f"Image file is empty: {img_file}"
    
    def test_fonts_exist(self):
        """Test that all font files exist and are not empty."""
        font_dir = DOCS_DIR / "_static" / "fonts"
        if not font_dir.exists():
            pytest.skip(f"Fonts directory not found: {font_dir}")
        
        # Check all font files
        for ext in ['*.woff', '*.woff2', '*.ttf', '*.eot', '*.otf']:
            for font_file in font_dir.glob(ext):
                assert font_file.is_file(), f"Font is not a file: {font_file}"
                assert font_file.stat().st_size > 0, f"Font file is empty: {font_file}"

class TestTemplates:
    """Tests for documentation templates."""
    
    def test_templates_directory_exists(self):
        """Test that the templates directory exists."""
        templates_dir = DOCS_DIR / "_templates"
        assert templates_dir.exists(), f"Templates directory not found: {templates_dir}"
        assert templates_dir.is_dir(), f"Templates directory is not a directory: {templates_dir}"
    
    def test_layout_template_exists(self):
        """Test that the layout template exists."""
        layout_file = DOCS_DIR / "_templates" / "layout.html"
        assert layout_file.exists(), f"Layout template not found: {layout_file}"
        assert layout_file.is_file(), f"Layout template is not a file: {layout_file}"
        
        # Check that the file is not empty
        assert layout_file.stat().st_size > 0, f"Layout template is empty: {layout_file}"
    
    def test_layout_includes_static_files(self):
        """Test that the layout includes the static files."""
        layout_file = DOCS_DIR / "_templates" / "layout.html"
        assert layout_file.exists(), f"Layout template not found: {layout_file}"
        
        # Read the layout file
        content = layout_file.read_text(encoding='utf-8')
        
        # Check for CSS and JS includes
        assert "theme.css" in content, "Theme CSS not included in layout"
        assert "theme.js" in content, "Theme JavaScript not included in layout"
    
    def test_layout_has_required_blocks(self):
        """Test that the layout has the required template blocks."""
        layout_file = DOCS_DIR / "_templates" / "layout.html"
        assert layout_file.exists(), f"Layout template not found: {layout_file}"
        
        # Read the layout file
        content = layout_file.read_text(encoding='utf-8')
        
        # Check for required blocks
        required_blocks = [
            '{% block doctype %}',
            '{% block htmltag %}',
            '{% block head %}',
            '{% block body %}',
            '{% block header %}',
            '{% block content %}',
            '{% block footer %}',
            '{% block scripts %}',
        ]
        
        for block in required_blocks:
            assert block in content, f"Required block not found in layout: {block}"

if __name__ == "__main__":
    pytest.main([__file__])
