"""
PROBLEM: Longest Substring Without Repeating Characters (LeetCode 3)
Difficulty: Medium
Pattern: Sliding Window, Hash Map
Companies: Amazon, Facebook, Google, Microsoft, Apple, Bloomberg

Given a string s, find the length of the longest substring without repeating characters.

Example 1:
    Input: s = "abcabcbb"
    Output: 3
    Explanation: The answer is "abc", with the length of 3

Example 2:
    Input: s = "bbbbb"
    Output: 1
    Explanation: The answer is "b", with the length of 1

Example 3:
    Input: s = "pwwkew"
    Output: 3
    Explanation: The answer is "wke", with the length of 3

Constraints:
- 0 <= s.length <= 5 * 10^4
- s consists of English letters, digits, symbols and spaces

Approach:
1. Use sliding window with hash set
2. Expand right pointer to include new characters
3. If duplicate found, shrink from left until duplicate removed
4. Track maximum window size

Time: O(n) - each character visited at most twice
Space: O(min(n, m)) where m is charset size
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_set = set()
        left = 0
        max_length = 0

        for right in range(len(s)):
            # Shrink window until no duplicate
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1

            # Add current character
            char_set.add(s[right])

            # Update max length
            max_length = max(max_length, right - left + 1)

        return max_length


# Tests
def test():
    sol = Solution()

    assert sol.lengthOfLongestSubstring("abcabcbb") == 3
    assert sol.lengthOfLongestSubstring("bbbbb") == 1
    assert sol.lengthOfLongestSubstring("pwwkew") == 3
    assert sol.lengthOfLongestSubstring("") == 0
    assert sol.lengthOfLongestSubstring("au") == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
