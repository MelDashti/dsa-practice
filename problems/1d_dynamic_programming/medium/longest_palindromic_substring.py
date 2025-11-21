"""
PROBLEM: Longest Palindromic Substring (LeetCode 5)
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Microsoft, Apple, Facebook, Google

Given a string s, return the longest palindromic substring in s.

Example 1:
    Input: s = "babad"
    Output: "bab"
    Explanation: "aba" is also a valid answer.

Example 2:
    Input: s = "cbbd"
    Output: "bb"

Constraints:
- 1 <= s.length <= 1000
- s consist of only digits and English letters

Approach:
1. Expand around center approach is most efficient
2. A palindrome mirrors around its center
3. For each character, try to expand around it as center
4. Handle both odd length (single center) and even length (two centers)
5. Track the longest palindrome found

Alternative: Dynamic Programming
- dp[i][j] = true if substring s[i:j+1] is palindrome
- dp[i][j] = (s[i] == s[j]) and (j - i <= 2 or dp[i+1][j-1])

Time: O(n^2) - expand around each center
Space: O(1) - only store indices
"""


class Solution:
    def longest_palindrome(self, s: str) -> str:
        if not s:
            return ""

        start = 0
        max_len = 0

        def expand_around_center(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # Return length of palindrome
            return right - left - 1

        for i in range(len(s)):
            # Check for odd length palindrome (single center)
            len1 = expand_around_center(i, i)
            # Check for even length palindrome (two centers)
            len2 = expand_around_center(i, i + 1)

            # Get maximum length palindrome at this position
            curr_len = max(len1, len2)

            # Update if we found a longer palindrome
            if curr_len > max_len:
                max_len = curr_len
                # Calculate start position of palindrome
                start = i - (curr_len - 1) // 2

        return s[start:start + max_len]


# Tests
def test():
    sol = Solution()

    result1 = sol.longest_palindrome("babad")
    assert result1 in ["bab", "aba"]

    assert sol.longest_palindrome("cbbd") == "bb"
    assert sol.longest_palindrome("a") == "a"
    assert sol.longest_palindrome("ac") == "a" or sol.longest_palindrome("ac") == "c"
    assert sol.longest_palindrome("racecar") == "racecar"
    assert sol.longest_palindrome("noon") == "noon"

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
