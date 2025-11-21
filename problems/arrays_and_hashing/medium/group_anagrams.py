"""
PROBLEM: Group Anagrams (LeetCode 49)
LeetCode: https://leetcode.com/problems/group-anagrams/
Difficulty: Medium
Pattern: Arrays & Hashing
Companies: Amazon, Facebook, Google, Microsoft, Uber

Given an array of strings strs, group the anagrams together. You can return
the answer in any order.

An anagram is a word formed by rearranging the letters of a different word,
using all the original letters exactly once.

Example 1:
    Input: strs = ["eat","tea","tan","ate","nat","bat"]
    Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Example 2:
    Input: strs = [""]
    Output: [[""]]

Example 3:
    Input: strs = ["a"]
    Output: [["a"]]

Constraints:
- 1 <= strs.length <= 10^4
- 0 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters

Approach:
1. Use hash map where key is sorted string (canonical form)
2. For each string, sort it to get the key
3. Add original string to the list at that key
4. Return all values from the hash map

Alternative: Use character count array as key instead of sorting

Time: O(n * k log k) where n is number of strings, k is max length
Space: O(n * k) for the hash map
"""

from typing import List
from collections import defaultdict


class Solution:
    def group_anagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_map = defaultdict(list)

        for s in strs:
            # Sort the string to create a key
            key = ''.join(sorted(s))
            anagram_map[key].append(s)

        return list(anagram_map.values())

    # Alternative using character count
    def groupAnagrams_v2(self, strs: List[str]) -> List[List[str]]:
        anagram_map = defaultdict(list)

        for s in strs:
            # Create count array as key
            count = [0] * 26
            for char in s:
                count[ord(char) - ord('a')] += 1
            key = tuple(count)
            anagram_map[key].append(s)

        return list(anagram_map.values())


# Tests
def test():
    sol = Solution()

    result1 = sol.group_anagrams(["eat","tea","tan","ate","nat","bat"])
    # Sort for comparison
    result1_sorted = [sorted(group) for group in result1]
    expected1_sorted = [sorted(group) for group in [["bat"],["nat","tan"],["ate","eat","tea"]]]
    assert sorted(result1_sorted) == sorted(expected1_sorted)

    assert sol.group_anagrams([""]) == [[""]]
    assert sol.group_anagrams(["a"]) == [["a"]]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
