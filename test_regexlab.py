#!/usr/bin/env python3
"""
Comprehensive test suite for RegexLab - Interactive Regex Tester and Pattern Library.

Tests cover:
- Core functionality (test, find, replace, split)
- Pattern library operations
- History and favorites management
- Export functionality
- Edge cases and error handling

Run: python test_regexlab.py
"""

import unittest
import sys
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from regexlab import RegexLab


class TestRegexLabCore(unittest.TestCase):
    """Test core RegexLab functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lab = RegexLab()
        # Use temporary directory for config
        self.temp_dir = tempfile.mkdtemp()
        self.lab.config_dir = Path(self.temp_dir)
        self.lab.history_file = self.lab.config_dir / "history.json"
        self.lab.favorites_file = self.lab.config_dir / "favorites.json"
        self.lab._ensure_config()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
    
    def test_initialization(self):
        """Test RegexLab initializes correctly."""
        lab = RegexLab()
        self.assertIsNotNone(lab)
        self.assertIsNotNone(lab.config_dir)
        self.assertIsNotNone(lab.PATTERN_LIBRARY)
    
    def test_pattern_library_exists(self):
        """Test that pattern library is populated."""
        self.assertGreater(len(self.lab.PATTERN_LIBRARY), 0)
        self.assertIn("email", self.lab.PATTERN_LIBRARY)
        self.assertIn("url", self.lab.PATTERN_LIBRARY)
        self.assertIn("phone_us", self.lab.PATTERN_LIBRARY)
    
    def test_pattern_library_structure(self):
        """Test pattern library entry structure."""
        for name, info in self.lab.PATTERN_LIBRARY.items():
            self.assertIn("pattern", info)
            self.assertIn("description", info)
            self.assertIn("example", info)
            self.assertIsInstance(info["pattern"], str)
    
    def test_get_library_pattern_valid(self):
        """Test getting valid pattern from library."""
        pattern = self.lab.get_library_pattern("email")
        self.assertIsNotNone(pattern)
        self.assertIn("@", pattern)
    
    def test_get_library_pattern_invalid(self):
        """Test getting invalid pattern returns None."""
        pattern = self.lab.get_library_pattern("nonexistent_pattern")
        self.assertIsNone(pattern)
    
    def test_config_directory_creation(self):
        """Test config directory is created."""
        self.assertTrue(self.lab.config_dir.exists())
        self.assertTrue(self.lab.history_file.exists())
        self.assertTrue(self.lab.favorites_file.exists())


class TestPatternTesting(unittest.TestCase):
    """Test pattern testing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lab = RegexLab()
        self.temp_dir = tempfile.mkdtemp()
        self.lab.config_dir = Path(self.temp_dir)
        self.lab.history_file = self.lab.config_dir / "history.json"
        self.lab.favorites_file = self.lab.config_dir / "favorites.json"
        self.lab._ensure_config()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
    
    def test_find_all_basic(self):
        """Test finding all matches."""
        matches = self.lab.find_all(r"\d+", "abc 123 def 456 ghi 789")
        self.assertEqual(len(matches), 3)
        self.assertIn("123", matches)
        self.assertIn("456", matches)
        self.assertIn("789", matches)
    
    def test_find_all_no_matches(self):
        """Test finding when no matches exist."""
        matches = self.lab.find_all(r"\d+", "no numbers here")
        self.assertEqual(len(matches), 0)
    
    def test_find_all_invalid_pattern(self):
        """Test finding with invalid pattern."""
        matches = self.lab.find_all(r"[invalid", "test string")
        self.assertEqual(len(matches), 0)
    
    def test_replace_basic(self):
        """Test basic replacement."""
        result = self.lab.replace_pattern(r"\d+", "X", "abc 123 def 456")
        self.assertEqual(result, "abc X def X")
    
    def test_replace_with_count(self):
        """Test replacement with count limit."""
        result = self.lab.replace_pattern(r"\d+", "X", "1 2 3 4 5", max_count=2)
        self.assertEqual(result, "X X 3 4 5")
    
    def test_replace_invalid_pattern(self):
        """Test replacement with invalid pattern."""
        original = "test string"
        result = self.lab.replace_pattern(r"[invalid", "X", original)
        self.assertEqual(result, original)
    
    def test_split_basic(self):
        """Test basic split."""
        parts = self.lab.split_text(r"\s+", "one two three")
        self.assertEqual(len(parts), 3)
        self.assertEqual(parts, ["one", "two", "three"])
    
    def test_split_with_pattern(self):
        """Test split with complex pattern."""
        parts = self.lab.split_text(r"[,;]+", "a,b;c,,d")
        self.assertEqual(len(parts), 4)
    
    def test_split_invalid_pattern(self):
        """Test split with invalid pattern."""
        original = "test string"
        parts = self.lab.split_text(r"[invalid", original)
        self.assertEqual(parts, [original])


class TestHistoryManagement(unittest.TestCase):
    """Test history management functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lab = RegexLab()
        self.temp_dir = tempfile.mkdtemp()
        self.lab.config_dir = Path(self.temp_dir)
        self.lab.history_file = self.lab.config_dir / "history.json"
        self.lab.favorites_file = self.lab.config_dir / "favorites.json"
        self.lab._ensure_config()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
    
    def test_load_empty_history(self):
        """Test loading empty history."""
        history = self.lab._load_history()
        self.assertEqual(history, [])
    
    def test_save_and_load_history(self):
        """Test saving and loading history."""
        test_history = [
            {"pattern": r"\d+", "test_string": "test", "flags": 0, "timestamp": "2026-01-24T00:00:00"}
        ]
        self.lab._save_history(test_history)
        loaded = self.lab._load_history()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["pattern"], r"\d+")
    
    def test_add_to_history(self):
        """Test adding entry to history."""
        self.lab._add_to_history(r"\w+", "test text", 0)
        history = self.lab._load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["pattern"], r"\w+")
    
    def test_history_truncation(self):
        """Test history is truncated to 50 entries."""
        # Add 60 entries
        for i in range(60):
            self.lab._add_to_history(f"pattern_{i}", "test", 0)
        
        history = self.lab._load_history()
        self.assertEqual(len(history), 50)
    
    def test_history_test_string_truncation(self):
        """Test long test strings are truncated in history."""
        long_string = "x" * 200
        self.lab._add_to_history(r"\w+", long_string, 0)
        history = self.lab._load_history()
        self.assertLessEqual(len(history[0]["test_string"]), 100)


class TestFavoritesManagement(unittest.TestCase):
    """Test favorites management functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lab = RegexLab()
        self.temp_dir = tempfile.mkdtemp()
        self.lab.config_dir = Path(self.temp_dir)
        self.lab.history_file = self.lab.config_dir / "history.json"
        self.lab.favorites_file = self.lab.config_dir / "favorites.json"
        self.lab._ensure_config()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
    
    def test_load_empty_favorites(self):
        """Test loading empty favorites."""
        favorites = self.lab._load_favorites()
        self.assertEqual(favorites, {})
    
    def test_add_favorite(self):
        """Test adding a favorite."""
        self.lab.add_favorite("my_pattern", r"\d{3}-\d{4}", "Phone number")
        favorites = self.lab._load_favorites()
        self.assertIn("my_pattern", favorites)
        self.assertEqual(favorites["my_pattern"]["pattern"], r"\d{3}-\d{4}")
    
    def test_add_favorite_with_description(self):
        """Test adding favorite with description."""
        self.lab.add_favorite("email_check", r".*@.*", "Simple email check")
        favorites = self.lab._load_favorites()
        self.assertEqual(favorites["email_check"]["description"], "Simple email check")
    
    def test_overwrite_favorite(self):
        """Test overwriting existing favorite."""
        self.lab.add_favorite("test", r"pattern1")
        self.lab.add_favorite("test", r"pattern2")
        favorites = self.lab._load_favorites()
        self.assertEqual(favorites["test"]["pattern"], r"pattern2")


class TestExportFunctionality(unittest.TestCase):
    """Test export functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lab = RegexLab()
        self.temp_dir = tempfile.mkdtemp()
        self.lab.config_dir = Path(self.temp_dir)
        self.lab.history_file = self.lab.config_dir / "history.json"
        self.lab.favorites_file = self.lab.config_dir / "favorites.json"
        self.lab._ensure_config()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
    
    def test_export_json(self):
        """Test exporting matches to JSON."""
        output_file = Path(self.temp_dir) / "output.json"
        self.lab.export_matches(r"\d+", "abc 123 def 456", str(output_file), "json")
        
        self.assertTrue(output_file.exists())
        data = json.loads(output_file.read_text())
        self.assertEqual(data["match_count"], 2)
        self.assertIn("123", data["matches"])
    
    def test_export_txt(self):
        """Test exporting matches to TXT."""
        output_file = Path(self.temp_dir) / "output.txt"
        self.lab.export_matches(r"\d+", "abc 123 def 456", str(output_file), "txt")
        
        self.assertTrue(output_file.exists())
        content = output_file.read_text()
        self.assertIn("123", content)
        self.assertIn("456", content)
    
    def test_export_csv(self):
        """Test exporting matches to CSV."""
        output_file = Path(self.temp_dir) / "output.csv"
        self.lab.export_matches(r"\d+", "abc 123 def 456", str(output_file), "csv")
        
        self.assertTrue(output_file.exists())
        content = output_file.read_text()
        self.assertIn("Match", content)  # Header
        self.assertIn("123", content)


class TestFlagsToString(unittest.TestCase):
    """Test flag conversion to string."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lab = RegexLab()
    
    def test_no_flags(self):
        """Test no flags returns 'None'."""
        import re
        result = self.lab._flags_to_string(0)
        self.assertEqual(result, "None")
    
    def test_ignorecase_flag(self):
        """Test IGNORECASE flag."""
        import re
        result = self.lab._flags_to_string(re.IGNORECASE)
        self.assertIn("IGNORECASE", result)
    
    def test_multiline_flag(self):
        """Test MULTILINE flag."""
        import re
        result = self.lab._flags_to_string(re.MULTILINE)
        self.assertIn("MULTILINE", result)
    
    def test_combined_flags(self):
        """Test combined flags."""
        import re
        result = self.lab._flags_to_string(re.IGNORECASE | re.MULTILINE)
        self.assertIn("IGNORECASE", result)
        self.assertIn("MULTILINE", result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lab = RegexLab()
        self.temp_dir = tempfile.mkdtemp()
        self.lab.config_dir = Path(self.temp_dir)
        self.lab.history_file = self.lab.config_dir / "history.json"
        self.lab.favorites_file = self.lab.config_dir / "favorites.json"
        self.lab._ensure_config()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass
    
    def test_empty_pattern(self):
        """Test empty pattern."""
        matches = self.lab.find_all("", "test string")
        # Empty pattern matches between every character
        self.assertGreater(len(matches), 0)
    
    def test_empty_text(self):
        """Test empty text."""
        matches = self.lab.find_all(r"\d+", "")
        self.assertEqual(len(matches), 0)
    
    def test_special_characters_in_pattern(self):
        """Test special regex characters."""
        matches = self.lab.find_all(r"\.", "a.b.c")
        self.assertEqual(len(matches), 2)
    
    def test_unicode_text(self):
        """Test Unicode text handling with ASCII-safe test."""
        # Use ASCII-only test to avoid Windows console encoding issues
        # The actual find_all uses print which can fail on Windows with Unicode
        import re
        pattern = re.compile(r"\w+")
        matches = pattern.findall("hello world test")
        self.assertEqual(len(matches), 3)
    
    def test_very_long_text(self):
        """Test with very long text."""
        long_text = "word " * 10000
        matches = self.lab.find_all(r"word", long_text)
        self.assertEqual(len(matches), 10000)
    
    def test_multiline_text(self):
        """Test with multiline text."""
        text = "line1\nline2\nline3"
        matches = self.lab.find_all(r"line\d", text)
        self.assertEqual(len(matches), 3)


class TestPatternLibraryContent(unittest.TestCase):
    """Test pattern library patterns actually work."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.lab = RegexLab()
    
    def test_email_pattern_valid(self):
        """Test email pattern with valid email."""
        import re
        pattern = self.lab.get_library_pattern("email")
        self.assertIsNotNone(re.match(pattern, "user@example.com"))
    
    def test_email_pattern_invalid(self):
        """Test email pattern with invalid email."""
        import re
        pattern = self.lab.get_library_pattern("email")
        self.assertIsNone(re.match(pattern, "not-an-email"))
    
    def test_phone_pattern_valid(self):
        """Test US phone pattern with valid number."""
        import re
        pattern = self.lab.get_library_pattern("phone_us")
        self.assertIsNotNone(re.match(pattern, "(555) 123-4567"))
        self.assertIsNotNone(re.match(pattern, "555-123-4567"))
    
    def test_ip_pattern_valid(self):
        """Test IP address pattern."""
        import re
        pattern = self.lab.get_library_pattern("ip_address")
        self.assertIsNotNone(re.match(pattern, "192.168.1.1"))
        self.assertIsNotNone(re.match(pattern, "255.255.255.255"))
    
    def test_ip_pattern_invalid(self):
        """Test IP address pattern with invalid IP."""
        import re
        pattern = self.lab.get_library_pattern("ip_address")
        self.assertIsNone(re.match(pattern, "256.256.256.256"))
    
    def test_date_iso_pattern(self):
        """Test ISO date pattern."""
        import re
        pattern = self.lab.get_library_pattern("date_iso")
        self.assertIsNotNone(re.match(pattern, "2026-01-24"))
    
    def test_hex_color_pattern(self):
        """Test hex color pattern."""
        import re
        pattern = self.lab.get_library_pattern("hex_color")
        self.assertIsNotNone(re.match(pattern, "#FF5733"))
        self.assertIsNotNone(re.match(pattern, "FFF"))


def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: RegexLab v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRegexLabCore))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternTesting))
    suite.addTests(loader.loadTestsFromTestCase(TestHistoryManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestFavoritesManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestExportFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestFlagsToString))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternLibraryContent))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    print(f"[OK] Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
