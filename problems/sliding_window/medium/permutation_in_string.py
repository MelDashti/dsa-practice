"""
PROBLEM: Permutation in String (LeetCode 567)
Difficulty: Medium
Pattern: Sliding Window, Hash Map
Companies: Amazon, Facebook, Google, Microsoft

Given two strings s1 and s2, return true if s2 contains a permutation of s1,
or false otherwise.

In other words, return true if one of s1's permutations is the substring of s2.

Example 1:
    Input: s1 = "ab", s2 = "eidbaooo"
    Output: true
    Explanation: s2 contains one permutation of s1 ("ba")

Example 2:
    Input: s1 = "ab", s2 = "eidboaoo"
    Output: false

Constraints:
- 1 <= s1.length, s2.length <= 10^4
- s1 and s2 consist of lowercase English letters

Approach:
1. Create frequency map of s1
2. Use sliding window of size len(s1) on s2
3. Check if window's frequency matches s1's frequency
4. Slide window and update frequencies

Time: O(n) where n is length of s2
Space: O(1) - fixed 26 letters
"""

from collections import Counter


class Solution:
    def check_inclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        s1_count = Counter(s1)
        window_count = Counter(s2[:len(s1)])

        # Check first window
        if s1_count == window_count:
            return True

        # Slide the window
        for i in range(len(s1), len(s2)):
            # Add new character to window
            window_count[s2[i]] += 1

            # Remove leftmost character from window
            left_char = s2[i - len(s1)]
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]

            # Check if current window matches
            if s1_count == window_count:
                return True

        return False


# Tests
def test():
    sol = Solution()

    assert sol.check_inclusion("ab", "eidbaooo") == True
    assert sol.check_inclusion("ab", "eidboaoo") == False
    assert sol.check_inclusion("abc", "bbbca") == True
    assert sol.check_inclusion("hello", "ooolleoooleh") == False

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
