"""
PROBLEM: Word Break (LeetCode 139)
Difficulty: Medium
Pattern: 1-D Dynamic Programming
Companies: Amazon, Google, Facebook, Microsoft, Apple

Given a string s and a dictionary of strings wordDict, return true if s can be
segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the
segmentation.

Example 1:
    Input: s = "leetcode", wordDict = ["leet","code"]
    Output: true
    Explanation: Return true because "leetcode" can be segmented as "leet code".

Example 2:
    Input: s = "applepenapple", wordDict = ["apple","pen"]
    Output: true
    Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
    Note that you are allowed to reuse a dictionary word.

Example 3:
    Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
    Output: false

Constraints:
- 1 <= s.length <= 300
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 20
- s and wordDict[i] consist of only lowercase English letters
- All the strings of wordDict are unique

Approach:
1. Use dynamic programming with boolean array
2. dp[i] = true if s[0:i] can be segmented
3. For each position i, check all previous positions j
4. If dp[j] is true and s[j:i] is in wordDict, then dp[i] = true
5. Convert wordDict to set for O(1) lookup
6. Base case: dp[0] = true (empty string)

Time: O(n^2 * m) - n^2 substrings, m for substring check
Space: O(n) - dp array
"""

from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # Convert to set for O(1) lookup
        word_set = set(wordDict)
        n = len(s)

        # dp[i] represents if s[0:i] can be segmented
        dp = [False] * (n + 1)
        dp[0] = True  # Empty string

        # Check each position
        for i in range(1, n + 1):
            # Try all possible previous positions
            for j in range(i):
                # If s[0:j] can be segmented and s[j:i] is a word
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break

        return dp[n]


# Tests
def test():
    sol = Solution()

    assert sol.wordBreak("leetcode", ["leet","code"]) == True
    assert sol.wordBreak("applepenapple", ["apple","pen"]) == True
    assert sol.wordBreak("catsandog", ["cats","dog","sand","and","cat"]) == False
    assert sol.wordBreak("a", ["a"]) == True
    assert sol.wordBreak("ab", ["a","b"]) == True
    assert sol.wordBreak("cars", ["car","ca","rs"]) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
