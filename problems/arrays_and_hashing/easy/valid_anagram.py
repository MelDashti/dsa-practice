"""
PROBLEM: Valid Anagram (LeetCode 242)
LeetCode: https://leetcode.com/problems/valid-anagram/
Difficulty: Easy
Pattern: Arrays & Hashing

Given two strings s and t, return true if t is an anagram of s, and false otherwise.
An anagram is a word formed by rearranging the letters of another word, using all
the original letters exactly once.

Example 1:
    Input: s = "anagram", t = "nagaram"
    Output: true

Example 2:
    Input: s = "rat", t = "car"
    Output: false

Constraints:
- 1 <= s.length, t.length <= 5 * 10^4
- s and t consist of lowercase English letters

Approach:
1. Check if lengths are equal (if not, can't be anagram)
2. Count frequency of each character in both strings
3. Compare the frequency maps
4. Alternative: Sort both strings and compare

Time: O(n) where n is length of string
Space: O(1) since we only have 26 lowercase letters
"""

from collections import Counter


class Solution:
    def is_anagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        return Counter(s) == Counter(t)

    # Alternative solution using sorting
    def isAnagram_v2(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)


# Tests
def test():
    sol = Solution()

    assert sol.is_anagram("anagram", "nagaram") == True
    assert sol.is_anagram("rat", "car") == False
    assert sol.is_anagram("listen", "silent") == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
