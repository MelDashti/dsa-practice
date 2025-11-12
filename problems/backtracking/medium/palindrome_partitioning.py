"""
PROBLEM: Palindrome Partitioning (LeetCode 131)
Difficulty: Medium
Pattern: Backtracking
Companies: Amazon, Microsoft, Apple, Facebook, Google

Given a string s, partition s such that every substring of the partition is a
palindrome. Return all possible palindrome partitioning of s.

Example 1:
    Input: s = "aab"
    Output: [["a","a","b"],["aa","b"]]

Example 2:
    Input: s = "a"
    Output: [["a"]]

Constraints:
- 1 <= s.length <= 16
- s contains only lowercase English letters

Approach:
1. Use backtracking to explore all possible partitions
2. At each position, try all possible substrings from current position
3. If substring is palindrome, add to current partition and recurse
4. Base case: when we reach end of string, add current partition to result
5. Helper function to check if string is palindrome
6. Backtrack by removing last added substring

Time: O(n * 2^n) - 2^n possible partitions, O(n) to check palindrome
Space: O(n) - recursion depth
"""

from typing import List


class Solution:
    def partition(self, s: str) -> List[List[str]]:
        result = []
        current = []

        def is_palindrome(string):
            return string == string[::-1]

        def backtrack(start):
            # Base case: reached end of string
            if start == len(s):
                result.append(current[:])
                return

            # Try all possible substrings starting from current position
            for end in range(start + 1, len(s) + 1):
                substring = s[start:end]
                if is_palindrome(substring):
                    current.append(substring)
                    backtrack(end)
                    current.pop()

        backtrack(0)
        return result


# Tests
def test():
    sol = Solution()

    # Test case 1
    result1 = sol.partition("aab")
    expected1 = [["a","a","b"],["aa","b"]]
    assert sorted([sorted(x) for x in result1]) == sorted([sorted(x) for x in expected1])

    # Test case 2
    result2 = sol.partition("a")
    expected2 = [["a"]]
    assert result2 == expected2

    # Test case 3
    result3 = sol.partition("aaa")
    expected3 = [["a","a","a"],["a","aa"],["aa","a"],["aaa"]]
    assert sorted([sorted(x) for x in result3]) == sorted([sorted(x) for x in expected3])

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
