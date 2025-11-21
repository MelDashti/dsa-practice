"""
PROBLEM: Distinct Subsequences (LeetCode 115)
Difficulty: Hard
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

Given two strings s and t, return the number of distinct subsequences of s which
equals t.

The test cases are generated so that the answer fits on a 32-bit signed integer.

Example 1:
    Input: s = "rabbbit", t = "rabbit"
    Output: 3
    Explanation:
    As shown below, there are 3 ways you can generate "rabbit" from s.
    rabbbit
    rabbbit
    rabbbit

Example 2:
    Input: s = "babgbag", t = "bag"
    Output: 5
    Explanation:
    As shown below, there are 5 ways you can generate "bag" from s.
    babgbag
    babgbag
    babgbag
    babgbag
    babgbag

Constraints:
- 1 <= s.length, t.length <= 1000
- s and t consist of English letters.

Approach:
1. Use 2D DP where dp[i][j] = number of distinct subsequences of s[0:i] that
   equal t[0:j]
2. Base case: dp[i][0] = 1 for all i (empty string has one subsequence: empty)
3. Base case: dp[0][j] = 0 for j > 0 (can't form non-empty t from empty s)
4. If s[i-1] == t[j-1]:
   - dp[i][j] = dp[i-1][j-1] (use this character) + dp[i-1][j] (skip)
5. Else:
   - dp[i][j] = dp[i-1][j] (skip this character)
6. Can optimize to 1D array

Time: O(m * n) - where m and n are lengths of s and t
Space: O(n) - 1D DP array
"""


class Solution:
    def num_distinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)

        # dp[i][j] = number of ways to form t[0:j] from s[0:i]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base case: empty t can be formed in one way (select nothing)
        for i in range(m + 1):
            dp[i][0] = 1

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Always have option to skip current character in s
                dp[i][j] = dp[i - 1][j]

                # If characters match, add option to use current character
                if s[i - 1] == t[j - 1]:
                    dp[i][j] += dp[i - 1][j - 1]

        return dp[m][n]


# Tests
def test():
    sol = Solution()

    assert sol.num_distinct("rabbbit", "rabbit") == 3
    assert sol.num_distinct("babgbag", "bag") == 5
    assert sol.num_distinct("abc", "abc") == 1
    assert sol.num_distinct("abc", "def") == 0
    assert sol.num_distinct("aaa", "a") == 3
    assert sol.num_distinct("", "") == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
