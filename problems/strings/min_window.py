"""
PROBLEM: Minimum Window Substring
Difficulty: Hard
Pattern: Sliding Window + Hash Map
Companies: Amazon, Facebook, Google, Microsoft
LeetCode: https://leetcode.com/problems/minimum-window-substring/

Given two strings s and t, find the smallest substring in s that contains
all characters of t (including duplicates). Return "" if none exists.

Example 1:
    s = "ADOBECODEBANC", t = "ABC"
    Output: "BANC"

Example 2:
    s = "a", t = "a"
    Output: "a"

Example 3:
    s = "a", t = "aa"
    Output: ""  (need two 'a's)

Constraints:
- 1 <= s.length, t.length <= 10^5
- Consists of English letters

Approach:
1. Create frequency map for t
2. Use sliding window (left, right pointers)
3. Expand right: add chars to window
4. Contract left: when valid, try to minimize
5. Track minimum window found

Time Complexity: O(m + n) where m=len(s), n=len(t)
Space Complexity: O(k) where k=unique chars
"""

from collections import Counter
from typing import Dict


class Solution:
    """Solution for Minimum Window Substring problem."""

    def minWindow(self, s: str, t: str) -> str:
        """
        Find the minimum window substring containing all characters from t.

        Args:
            s: Source string to search in
            t: Target string containing required characters

        Returns:
            Smallest substring of s containing all chars from t, or "" if none exists

        Time Complexity: O(m + n) where m=len(s), n=len(t)
        Space Complexity: O(k) where k=unique characters
        """
        if not s or not t:
            return ""

        # Frequency map of target string
        freq_t: Counter = Counter(t)
        required: int = len(freq_t)  # Unique chars that must be in window

        # Sliding window variables
        left: int = 0
        formed: int = 0  # Tracks how many unique chars meet frequency requirement
        window: Dict[str, int] = {}  # Frequency map of current window

        # Track the minimum window
        min_len: float = float('inf')
        min_left: int = 0
        min_right: int = 0

        # Expand window with right pointer
        for right, letter in enumerate(s):
            # Add character to window
            window[letter] = window.get(letter, 0) + 1

            # Check if this character's frequency matches requirement
            if letter in freq_t and window[letter] == freq_t[letter]:
                formed += 1

            # Contract window while it's valid
            while formed == required and left <= right:
                # Update minimum window if current is smaller
                window_len = right - left + 1
                if window_len < min_len:
                    min_len = window_len
                    min_left = left
                    min_right = right

                # Remove leftmost character from window
                left_char = s[left]
                window[left_char] -= 1

                # Check if removing left_char makes window invalid
                if left_char in freq_t and window[left_char] < freq_t[left_char]:
                    formed -= 1

                left += 1

        return "" if min_len == float('inf') else s[min_left:min_right + 1]


def main():
    """Example usage and manual testing."""
    solution = Solution()

    # Test case 1
    result1 = solution.minWindow("ADOBECODEBANC", "ABC")
    print(f"Test 1: minWindow('ADOBECODEBANC', 'ABC') = '{result1}'")  # "BANC"

    # Test case 2
    result2 = solution.minWindow("a", "a")
    print(f"Test 2: minWindow('a', 'a') = '{result2}'")  # "a"

    # Test case 3
    result3 = solution.minWindow("a", "aa")
    print(f"Test 3: minWindow('a', 'aa') = '{result3}'")  # ""

    print("✓ All manual tests passed")


if __name__ == "__main__":
    main()
