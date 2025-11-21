"""
PROBLEM: Regular Expression Matching (LeetCode 10)
LeetCode: https://leetcode.com/problems/regular-expression-matching/
Difficulty: Hard
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

Given an input string s and a pattern p, implement regular expression matching
with support for '.' and '*' where:

- '.' Matches any single character.
- '*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

Example 1:
    Input: s = "aa", p = "a"
    Output: false
    Explanation: "a" does not match the entire string "aa".

Example 2:
    Input: s = "aa", p = "a*"
    Output: true
    Explanation: '*' means zero or more of the preceding element, 'a'.
    Therefore, by repeating 'a' once, it becomes "aa".

Example 3:
    Input: s = "ab", p = ".*"
    Output: true
    Explanation: ".*" means "zero or more (*) of any character (.)".

Constraints:
- 1 <= s.length <= 20
- 1 <= p.length <= 20
- s contains only lowercase English letters.
- p contains only lowercase English letters, '.', and '*'.
- It is guaranteed for each appearance of the character '*', there will be a
  previous valid character to match.

Approach:
1. Use 2D DP where dp[i][j] = whether s[0:i] matches p[0:j]
2. Base case: dp[0][0] = True (empty string matches empty pattern)
3. Handle patterns with '*' that can match empty string
4. Two cases:
   a) If p[j-1] is not '*':
      - Characters must match: s[i-1] == p[j-1] or p[j-1] == '.'
      - dp[i][j] = dp[i-1][j-1]
   b) If p[j-1] is '*':
      - Match zero occurrences: dp[i][j] = dp[i][j-2]
      - Match one or more: if s[i-1] matches p[j-2], dp[i][j] |= dp[i-1][j]

Time: O(m * n) - where m and n are lengths of s and p
Space: O(m * n) - DP table
"""


class Solution:
    def is_match(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)

        # dp[i][j] = whether s[0:i] matches p[0:j]
        dp = [[False] * (n + 1) for _ in range(m + 1)]

        # Base case: empty string matches empty pattern
        dp[0][0] = True

        # Handle patterns like a*, a*b*, a*b*c* that can match empty string
        for j in range(2, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == '*':
                    # '*' can match zero occurrences of preceding character
                    dp[i][j] = dp[i][j - 2]

                    # '*' can match one or more occurrences if characters match
                    if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                        dp[i][j] = dp[i][j] or dp[i - 1][j]
                else:
                    # Characters must match (or pattern has '.')
                    if p[j - 1] == s[i - 1] or p[j - 1] == '.':
                        dp[i][j] = dp[i - 1][j - 1]

        return dp[m][n]


# Tests
def test():
    sol = Solution()

    assert sol.is_match("aa", "a") == False
    assert sol.is_match("aa", "a*") == True
    assert sol.is_match("ab", ".*") == True
    assert sol.is_match("aab", "c*a*b") == True
    assert sol.is_match("mississippi", "mis*is*p*.") == False
    assert sol.is_match("", "") == True
    assert sol.is_match("", "a*") == True
    assert sol.is_match("a", "ab*") == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
