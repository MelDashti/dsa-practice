"""Tests for Minimum Window Substring implementation."""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from problems.strings.min_window import Solution


class TestMinWindow:
    """Test suite for minimum window substring problem."""

    def setup_method(self):
        """Set up test fixtures."""
        self.solution = Solution()

    def test_basic_example(self):
        """Test basic example from problem statement."""
        result = self.solution.minWindow("ADOBECODEBANC", "ABC")
        assert result == "BANC"

    def test_single_character(self):
        """Test with single character strings."""
        assert self.solution.minWindow("a", "a") == "a"

    def test_impossible_case(self):
        """Test when target has more occurrences than source."""
        assert self.solution.minWindow("a", "aa") == ""

    def test_empty_strings(self):
        """Test with empty strings."""
        assert self.solution.minWindow("", "a") == ""
        assert self.solution.minWindow("a", "") == ""

    def test_target_longer_than_source(self):
        """Test when target is longer than source."""
        assert self.solution.minWindow("ab", "abc") == ""

    def test_duplicate_characters(self):
        """Test with duplicate characters in target."""
        result = self.solution.minWindow("aa", "aa")
        assert result == "aa"

    def test_entire_string_needed(self):
        """Test when entire source string is the answer."""
        result = self.solution.minWindow("abc", "abc")
        assert result == "abc"

    def test_multiple_valid_windows(self):
        """Test when multiple valid windows exist (should return shortest)."""
        # "BANC" is shorter than "ADOBEC"
        result = self.solution.minWindow("ADOBECODEBANC", "ABC")
        assert len(result) == 4
        assert result == "BANC"

    def test_target_at_beginning(self):
        """Test when minimum window is at the beginning."""
        result = self.solution.minWindow("ABCDEF", "ABC")
        assert result == "ABC"

    def test_target_at_end(self):
        """Test when minimum window is at the end."""
        result = self.solution.minWindow("XYZABC", "ABC")
        assert result == "ABC"

    def test_case_sensitivity(self):
        """Test that solution is case-sensitive."""
        result = self.solution.minWindow("Aa", "AA")
        assert result == ""

    def test_long_string(self):
        """Test with longer strings."""
        s = "ABAACBAB"
        t = "ABC"
        result = self.solution.minWindow(s, t)
        assert result == "ACB" or result == "BAC"  # Either is valid
        assert len(result) == 3
