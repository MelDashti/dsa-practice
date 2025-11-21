"""
PROBLEM: Alien Dictionary (LeetCode 269)
LeetCode: https://leetcode.com/problems/alien-dictionary/
Difficulty: Hard
Pattern: Advanced Graphs, Topological Sort, DFS/BFS
Companies: Amazon, Google, Facebook, Airbnb, Microsoft

There is a new alien language that uses the English alphabet. However, the order
among the letters is unknown to you.

You are given a list of strings words from the alien language's dictionary, where
the strings in words are sorted lexicographically by the rules of this new language.

Return a string of the unique letters in the new alien language sorted in
lexicographically increasing order by the new language's rules. If there is no
solution, return "". If there are multiple solutions, return any of them.

A string s is lexicographically smaller than a string t if at the first letter where
they differ, the letter in s comes before the letter in t in the alien language. If
the first min(s.length, t.length) letters are the same, then s is smaller if and
only if s.length < t.length.

Example 1:
    Input: words = ["wrt","wrf","er","ett","rftt"]
    Output: "wertf"

Example 2:
    Input: words = ["z","x"]
    Output: "zx"

Example 3:
    Input: words = ["z","x","z"]
    Output: ""
    Explanation: The order is invalid, so return "".

Constraints:
- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consists of only lowercase English letters

Approach:
1. Build a directed graph where edge a -> b means a comes before b
2. Compare adjacent words to find character ordering
3. Use topological sort (DFS or BFS/Kahn's algorithm)
4. Detect cycles (invalid ordering)
5. Return topologically sorted characters

Time: O(C) where C is total length of all words
Space: O(1) or O(26) for the graph, as there are at most 26 letters
"""

from typing import List
from collections import defaultdict, deque


class Solution:
    def alien_order(self, words: List[str]) -> str:
        # Build adjacency list and in-degree count
        graph = defaultdict(set)
        in_degree = {char: 0 for word in words for char in word}

        # Build the graph by comparing adjacent words
        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]
            min_len = min(len(word1), len(word2))

            # Check for invalid case: word1 is prefix of word2 but longer
            if len(word1) > len(word2) and word1[:min_len] == word2[:min_len]:
                return ""

            # Find first differing character
            for j in range(min_len):
                if word1[j] != word2[j]:
                    if word2[j] not in graph[word1[j]]:
                        graph[word1[j]].add(word2[j])
                        in_degree[word2[j]] += 1
                    break

        # Topological sort using BFS (Kahn's algorithm)
        queue = deque([char for char in in_degree if in_degree[char] == 0])
        result = []

        while queue:
            char = queue.popleft()
            result.append(char)

            for neighbor in graph[char]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Check if all characters are included (no cycle)
        if len(result) != len(in_degree):
            return ""

        return "".join(result)


# Tests
def test():
    sol = Solution()

    # Test 1: Standard alien dictionary
    words1 = ["wrt", "wrf", "er", "ett", "rftt"]
    result1 = sol.alien_order(words1)
    assert result1 == "wertf"

    # Test 2: Simple ordering
    words2 = ["z", "x"]
    result2 = sol.alien_order(words2)
    assert result2 == "zx"

    # Test 3: Invalid ordering (cycle)
    words3 = ["z", "x", "z"]
    assert sol.alien_order(words3) == ""

    # Test 4: Single word
    words4 = ["abc"]
    result4 = sol.alien_order(words4)
    assert len(result4) == 3 and set(result4) == {'a', 'b', 'c'}

    # Test 5: Invalid - longer word is prefix
    words5 = ["abc", "ab"]
    assert sol.alien_order(words5) == ""

    # Test 6: All same character
    words6 = ["a", "a"]
    assert sol.alien_order(words6) == "a"

    # Test 7: Multiple characters
    words7 = ["baa", "abcd", "abca", "cab", "cad"]
    result7 = sol.alien_order(words7)
    # Valid result should have 'b' before 'a', 'd' before 'c', etc.
    assert len(result7) == 4 and set(result7) == {'a', 'b', 'c', 'd'}

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
