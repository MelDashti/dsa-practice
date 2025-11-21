"""
PROBLEM: Longest Common Subsequence (LeetCode 1143)
LeetCode: https://leetcode.com/problems/longest-common-subsequence/
Difficulty: Medium
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

Given two strings text1 and text2, return the length of their longest common
subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string
with some characters (can be none) deleted without changing the relative order
of the remaining characters.

For example, "ace" is a subsequence of "abcde".
A common subsequence of two strings is a subsequence that is common to both strings.

Example 1:
    Input: text1 = "abcde", text2 = "ace"
    Output: 3
    Explanation: The longest common subsequence is "ace" and its length is 3.

Example 2:
    Input: text1 = "abc", text2 = "abc"
    Output: 3
    Explanation: The longest common subsequence is "abc" and its length is 3.

Example 3:
    Input: text1 = "abc", text2 = "def"
    Output: 0
    Explanation: There is no such common subsequence, so the result is 0.

Constraints:
- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English characters.

Approach:
1. Use 2D DP where dp[i][j] = LCS length for text1[0:i] and text2[0:j]
2. If text1[i-1] == text2[j-1], then dp[i][j] = dp[i-1][j-1] + 1
3. Otherwise, dp[i][j] = max(dp[i-1][j], dp[i][j-1])
4. Base case: dp[0][j] = 0 and dp[i][0] = 0 (empty string has LCS 0)
5. Can optimize space to O(n) by only keeping one row

Time: O(m * n) - where m and n are lengths of text1 and text2
Space: O(n) - only store one row
"""


class Solution:
    def longest_common_subsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)

        # Create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    # Characters match, extend LCS
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    # Take max of excluding one character from either string
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]


# Tests
def test():
    sol = Solution()

    assert sol.longest_common_subsequence("abcde", "ace") == 3
    assert sol.longest_common_subsequence("abc", "abc") == 3
    assert sol.longest_common_subsequence("abc", "def") == 0
    assert sol.longest_common_subsequence("", "") == 0
    assert sol.longest_common_subsequence("a", "a") == 1
    assert sol.longest_common_subsequence("abcdef", "fedcba") == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
