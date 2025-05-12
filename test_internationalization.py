"""
Tests for internationalization and localization support in the documentation.

This module contains tests to verify that the documentation supports
internationalization (i18n) and localization (l10n) as required.
"""

import gettext
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

class TestInternationalization:
    """Tests for internationalization support."""
    
    def test_locale_directory_exists(self):
        """Test that the locale directory exists."""
        locale_dir = DOCS_DIR / "locale"
        assert locale_dir.exists(), f"Locale directory not found: {locale_dir}"
        assert locale_dir.is_dir(), f"Locale directory is not a directory: {locale_dir}"
    
    def test_locale_directories_exist(self):
        """Test that locale directories exist for all supported languages."""
        locale_dir = DOCS_DIR / "locale"
        if not locale_dir.exists():
            pytest.skip(f"Locale directory not found: {locale_dir}")
        
        # List of expected language codes (e.g., 'en', 'es', 'fr', etc.)
        expected_languages = [
            'en',  # English
            'es',  # Spanish
            'fr',  # French
            'de',  # German
            'ja',  # Japanese
            'zh_CN',  # Simplified Chinese
            'zh_TW',  # Traditional Chinese
        ]n        
        for lang in expected_languages:
            lang_dir = locale_dir / lang
            assert lang_dir.exists(), f"Language directory not found: {lang_dir}"
            assert lang_dir.is_dir(), f"Language directory is not a directory: {lang_dir}"
    
    def test_po_files_exist(self):
        """Test that .po files exist for all supported languages."""
        locale_dir = DOCS_DIR / "locale"
        if not locale_dir.exists():
            pytest.skip(f"Locale directory not found: {locale_dir}")
        
        # Find all language directories
        for lang_dir in locale_dir.iterdir():
            if not lang_dir.is_dir() or lang_dir.name == 'pot':
                continue
                
            po_file = lang_dir / "LC_MESSAGES" / "docs.po"
            assert po_file.exists(), f"PO file not found: {po_file}"
            assert po_file.stat().st_size > 0, f"PO file is empty: {po_file}"
    
    def test_mo_files_exist(self, built_docs):
        """Test that .mo files are generated in the built documentation."""
        locale_dir = built_docs / "_sources" / "locale"
        if not locale_dir.exists():
            locale_dir = built_docs / "locale"
            
        if not locale_dir.exists():
            pytest.skip(f"Locale directory not found in built documentation: {locale_dir}")
        
        # Find all language directories
        for lang_dir in locale_dir.iterdir():
            if not lang_dir.is_dir() or lang_dir.name == 'pot':
                continue
                
            mo_file = lang_dir / "LC_MESSAGES" / "docs.mo"
            assert mo_file.exists(), f"MO file not found: {mo_file}"
            assert mo_file.stat().st_size > 0, f"MO file is empty: {mo_file}"
    
    def test_translation_quality(self):
        """Test the quality of translations."""
        # This would test the quality of translations
        # In a real project, you would use a tool like translate-toolkit or transifex-client
        pass
    
    def test_rtl_support(self, built_docs):
        """Test that the documentation supports right-to-left (RTL) languages."""
        # This would test that the documentation supports RTL languages like Arabic and Hebrew
        # In a real project, you would check the CSS and HTML for RTL support
        pass

class TestLocalization:
    """Tests for localization support."""
    
    def test_date_formatting(self):
        """Test that dates are properly formatted according to the locale."""
        # This would test that dates are properly formatted according to the locale
        # In a real project, you would use the locale module to test date formatting
        pass
    
    def test_number_formatting(self):
        """Test that numbers are properly formatted according to the locale."""
        # This would test that numbers are properly formatted according to the locale
        # In a real project, you would use the locale module to test number formatting
        pass
    
    def test_currency_formatting(self):
        """Test that currency values are properly formatted according to the locale."""
        # This would test that currency values are properly formatted according to the locale
        # In a real project, you would use the locale module to test currency formatting
        pass

class TestLanguageSwitcher:
    """Tests for the language switcher in the documentation."""
    
    def test_language_switcher_exists(self, built_docs):
        """Test that the language switcher exists in the built documentation."""
        index_file = built_docs / "index.html"
        if not index_file.exists():
            pytest.skip("Index file not found in built documentation")
            
        with open(index_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        language_switcher = soup.find('div', {'class': 'language-switcher'})
        assert language_switcher is not None, "Language switcher not found in index page"
    
    def test_language_switcher_links(self, built_docs):
        """Test that the language switcher contains links to all supported languages."""
        index_file = built_docs / "index.html"
        if not index_file.exists():
            pytest.skip("Index file not found in built documentation")
            
        with open(index_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        language_switcher = soup.find('div', {'class': 'language-switcher'})
        if language_switcher is None:
            pytest.skip("Language switcher not found in index page")
            
        # List of expected language codes (e.g., 'en', 'es', 'fr', etc.)
        expected_languages = [
            'en',  # English
            'es',  # Spanish
            'fr',  # French
            'de',  # German
            'ja',  # Japanese
            'zh_CN',  # Simplified Chinese
            'zh_TW',  # Traditional Chinese
        ]
        
        # Check that links to all supported languages exist
        for lang in expected_languages:
            lang_link = language_switcher.find('a', {'hreflang': lang})
            assert lang_link is not None, f"Link to {lang} not found in language switcher"

if __name__ == "__main__":
    pytest.main([__file__])
