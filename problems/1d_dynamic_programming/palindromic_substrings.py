"""
PROBLEM: Palindromic Substrings (LeetCode 647)
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Facebook, Google, Microsoft, Apple

Given a string s, return the number of palindromic substrings in it.

A string is a palindrome when it reads the same backward as forward.

A substring is a contiguous sequence of characters within the string.

Example 1:
    Input: s = "abc"
    Output: 3
    Explanation: Three palindromic strings: "a", "b", "c".

Example 2:
    Input: s = "aaa"
    Output: 6
    Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".

Constraints:
- 1 <= s.length <= 1000
- s consists of lowercase English letters

Approach:
1. Expand around center for each possible center
2. A palindrome mirrors around its center
3. For each position, expand outward while characters match
4. Count all valid palindromes found
5. Handle both odd length (single center) and even length (two centers)

Time: O(n^2) - expand around each of n centers
Space: O(1) - only counter variable
"""


class Solution:
    def countSubstrings(self, s: str) -> int:
        count = 0

        def expand_around_center(left, right):
            nonlocal count
            while left >= 0 and right < len(s) and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1

        for i in range(len(s)):
            # Count odd length palindromes (single center)
            expand_around_center(i, i)
            # Count even length palindromes (two centers)
            expand_around_center(i, i + 1)

        return count


# Tests
def test():
    sol = Solution()

    assert sol.countSubstrings("abc") == 3
    assert sol.countSubstrings("aaa") == 6
    assert sol.countSubstrings("a") == 1
    assert sol.countSubstrings("ab") == 2
    assert sol.countSubstrings("aba") == 4
    assert sol.countSubstrings("racecar") == 10

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
