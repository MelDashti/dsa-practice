"""
PROBLEM: Interleaving String (LeetCode 97)
LeetCode: https://leetcode.com/problems/interleaving-string/
Difficulty: Medium
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of
s1 and s2.

An interleaving of two strings s and t is a configuration where s and t are
divided into n and m substrings respectively, such that:

- s = s1 + s2 + ... + sn
- t = t1 + t2 + ... + tm
- |n - m| <= 1
- The interleaving is s1 + t1 + s2 + t2 + s3 + t3 + ... or t1 + s1 + t2 + s2 + t3 + s3 + ...

Note: a + b is the concatenation of strings a and b.

Example 1:
    Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
    Output: true
    Explanation: One way to obtain s3 is:
    Split s1 into s1 = "aa" + "bc" + "c", and s2 into s2 = "dbbc" + "a".
    Interleaving the two splits, we get "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac".

Example 2:
    Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
    Output: false

Example 3:
    Input: s1 = "", s2 = "", s3 = ""
    Output: true

Constraints:
- 0 <= s1.length, s2.length <= 100
- 0 <= s3.length <= 200
- s1, s2, and s3 consist of lowercase English letters.

Approach:
1. Use 2D DP where dp[i][j] = true if s3[0:i+j] can be formed by interleaving
   s1[0:i] and s2[0:j]
2. Base case: dp[0][0] = true (empty strings interleave to empty)
3. Transitions:
   - If s1[i-1] == s3[i+j-1], dp[i][j] |= dp[i-1][j]
   - If s2[j-1] == s3[i+j-1], dp[i][j] |= dp[i][j-1]
4. Can optimize to 1D array

Time: O(m * n) - where m and n are lengths of s1 and s2
Space: O(n) - 1D DP array
"""


class Solution:
    def is_interleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n, l = len(s1), len(s2), len(s3)

        # Quick check: lengths must match
        if m + n != l:
            return False

        # dp[i][j] = whether s3[0:i+j] can be formed by s1[0:i] and s2[0:j]
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True

        # Fill first column (only using s1)
        for i in range(1, m + 1):
            dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]

        # Fill first row (only using s2)
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]

        # Fill rest of table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Check if we can use character from s1
                if s1[i - 1] == s3[i + j - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]

                # Check if we can use character from s2
                if s2[j - 1] == s3[i + j - 1]:
                    dp[i][j] = dp[i][j] or dp[i][j - 1]

        return dp[m][n]


# Tests
def test():
    sol = Solution()

    assert sol.is_interleave("aabcc", "dbbca", "aadbbcbcac") == True
    assert sol.is_interleave("aabcc", "dbbca", "aadbbbaccc") == False
    assert sol.is_interleave("", "", "") == True
    assert sol.is_interleave("a", "", "a") == True
    assert sol.is_interleave("", "b", "b") == True
    assert sol.is_interleave("abc", "def", "adbecf") == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
