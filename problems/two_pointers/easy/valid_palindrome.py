"""
PROBLEM: Valid Palindrome (LeetCode 125)
LeetCode: https://leetcode.com/problems/valid-palindrome/
Difficulty: Easy
Pattern: Two Pointers
Companies: Amazon, Facebook, Microsoft, Apple, Bloomberg

A phrase is a palindrome if, after converting all uppercase letters into lowercase
letters and removing all non-alphanumeric characters, it reads the same forward and
backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:
    Input: s = "A man, a plan, a canal: Panama"
    Output: true
    Explanation: "amanaplanacanalpanama" is a palindrome

Example 2:
    Input: s = "race a car"
    Output: false
    Explanation: "raceacar" is not a palindrome

Example 3:
    Input: s = " "
    Output: true
    Explanation: Empty string is considered a palindrome

Constraints:
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters

Approach:
1. Use two pointers, left and right
2. Skip non-alphanumeric characters
3. Compare characters (case-insensitive)
4. Move pointers towards center

Time: O(n) - single pass
Space: O(1) - constant space
"""


class Solution:
    def is_palindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1

        while left < right:
            # Skip non-alphanumeric from left
            while left < right and not s[left].isalnum():
                left += 1

            # Skip non-alphanumeric from right
            while left < right and not s[right].isalnum():
                right -= 1

            # Compare characters
            if s[left].lower() != s[right].lower():
                return False

            left += 1
            right -= 1

        return True


# Tests
def test():
    sol = Solution()

    assert sol.is_palindrome("A man, a plan, a canal: Panama") == True
    assert sol.is_palindrome("race a car") == False
    assert sol.is_palindrome(" ") == True
    assert sol.is_palindrome("ab_a") == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
