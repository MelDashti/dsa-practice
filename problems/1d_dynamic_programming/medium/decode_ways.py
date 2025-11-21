"""
PROBLEM: Decode Ways (LeetCode 91)
LeetCode: https://leetcode.com/problems/decode-ways/
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Facebook, Google, Microsoft, Apple

A message containing letters from A-Z can be encoded into numbers using the
following mapping:

'A' -> "1"
'B' -> "2"
...
'Z' -> "26"

To decode an encoded message, all the digits must be grouped then mapped back
into letters using the reverse of the mapping above (there may be multiple ways).

Given a string s containing only digits, return the number of ways to decode it.

Example 1:
    Input: s = "12"
    Output: 2
    Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).

Example 2:
    Input: s = "226"
    Output: 3
    Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).

Example 3:
    Input: s = "06"
    Output: 0
    Explanation: "06" cannot be mapped to "F" because of the leading zero.

Constraints:
- 1 <= s.length <= 100
- s contains only digits and may contain leading zero(s)

Approach:
1. Use dynamic programming similar to climbing stairs
2. dp[i] = number of ways to decode s[0:i]
3. If s[i-1] is valid (1-9), add dp[i-1]
4. If s[i-2:i] is valid (10-26), add dp[i-2]
5. Handle edge cases: leading zeros, invalid numbers
6. Optimize space by keeping only last two values

Time: O(n) - single pass through string
Space: O(1) - only store two variables
"""


class Solution:
    def num_decodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0

        n = len(s)
        # prev2 = dp[i-2], prev1 = dp[i-1]
        prev2 = 1  # Empty string has one way
        prev1 = 1  # First character (if valid)

        for i in range(1, n):
            current = 0

            # Check single digit (1-9)
            if s[i] != '0':
                current += prev1

            # Check two digits (10-26)
            two_digit = int(s[i-1:i+1])
            if 10 <= two_digit <= 26:
                current += prev2

            prev2 = prev1
            prev1 = current

        return prev1


# Tests
def test():
    sol = Solution()

    assert sol.num_decodings("12") == 2
    assert sol.num_decodings("226") == 3
    assert sol.num_decodings("06") == 0
    assert sol.num_decodings("0") == 0
    assert sol.num_decodings("10") == 1
    assert sol.num_decodings("27") == 1
    assert sol.num_decodings("2101") == 1
    assert sol.num_decodings("111111") == 13

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
