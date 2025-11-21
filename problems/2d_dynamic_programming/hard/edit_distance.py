"""
PROBLEM: Edit Distance (LeetCode 72)
LeetCode: https://leetcode.com/problems/edit-distance/
Difficulty: Hard
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

Given two strings word1 and word2, return the minimum number of operations
required to convert word1 to word2.

You have the following three operations permitted on a word:
- Insert a character
- Delete a character
- Replace a character

Example 1:
    Input: word1 = "horse", word2 = "ros"
    Output: 3
    Explanation:
    horse -> rorse (replace 'h' with 'r')
    rorse -> rose (remove 'r')
    rose -> ros (remove 'e')

Example 2:
    Input: word1 = "intention", word2 = "execution"
    Output: 5
    Explanation:
    intention -> inention (remove 't')
    inention -> enention (replace 'i' with 'e')
    enention -> exention (replace 'n' with 'x')
    exention -> exection (replace 'n' with 'c')
    exection -> execution (insert 'u')

Constraints:
- 0 <= word1.length, word2.length <= 500
- word1 and word2 consist of lowercase English letters.

Approach:
1. Use 2D DP where dp[i][j] = min operations to convert word1[0:i] to word2[0:j]
2. Base cases:
   - dp[0][j] = j (need j insertions to create word2[0:j] from empty string)
   - dp[i][0] = i (need i deletions to make word1[0:i] empty)
3. If word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1] (no operation needed)
4. Else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
   - dp[i-1][j] + 1: delete from word1
   - dp[i][j-1] + 1: insert into word1
   - dp[i-1][j-1] + 1: replace in word1
5. Can optimize to 1D array

Time: O(m * n) - where m and n are lengths of word1 and word2
Space: O(m * n) - DP table
"""


class Solution:
    def min_distance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)

        # dp[i][j] = min operations to convert word1[0:i] to word2[0:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base case: convert empty string to word2[0:j]
        for j in range(n + 1):
            dp[0][j] = j

        # Base case: convert word1[0:i] to empty string
        for i in range(m + 1):
            dp[i][0] = i

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    # Characters match, no operation needed
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Take minimum of three operations
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # Delete from word1
                        dp[i][j - 1],      # Insert into word1
                        dp[i - 1][j - 1]   # Replace in word1
                    )

        return dp[m][n]


# Tests
def test():
    sol = Solution()

    assert sol.min_distance("horse", "ros") == 3
    assert sol.min_distance("intention", "execution") == 5
    assert sol.min_distance("", "") == 0
    assert sol.min_distance("a", "") == 1
    assert sol.min_distance("", "a") == 1
    assert sol.min_distance("abc", "abc") == 0

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
