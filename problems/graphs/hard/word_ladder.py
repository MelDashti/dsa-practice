"""
PROBLEM: Word Ladder (LeetCode 127)
Difficulty: Hard
Pattern: Graphs (BFS)
Companies: Amazon, Google, Facebook, Microsoft, LinkedIn

A transformation sequence from word beginWord to word endWord using a dictionary wordList
is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:
- Every adjacent pair of words differs by a single letter
- Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList
- sk == endWord

Given two words, beginWord and endWord, and a dictionary wordList, return the number of words
in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

Example 1:
    Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
    Output: 5
    Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> "cog",
    which is 5 words long.

Example 2:
    Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
    Output: 0
    Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.

Constraints:
- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters
- beginWord != endWord
- All the words in wordList are unique

Approach:
1. Use BFS to find shortest path from beginWord to endWord
2. For each word, try changing each character to find valid next words
3. Only visit words that are in wordList
4. Track visited words to avoid cycles
5. Return level (number of transformations + 1) when endWord is found

Time: O(M^2 * N) - M is word length, N is number of words
Space: O(M * N) - queue and visited set
"""

from typing import List
from collections import deque


class Solution:
    def ladder_length(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        # Convert to set for O(1) lookup
        word_set = set(wordList)
        queue = deque([(beginWord, 1)])  # (word, level)
        visited = {beginWord}

        while queue:
            word, level = queue.popleft()

            # Check if we reached the end
            if word == endWord:
                return level

            # Try changing each character
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i+1:]

                    # Check if it's a valid next word
                    if next_word in word_set and next_word not in visited:
                        visited.add(next_word)
                        queue.append((next_word, level + 1))

        return 0  # No transformation sequence found


# Tests
def test():
    sol = Solution()

    # Test 1: Valid transformation
    assert sol.ladder_length("hit", "cog", ["hot","dot","dog","lot","log","cog"]) == 5

    # Test 2: EndWord not in wordList
    assert sol.ladder_length("hit", "cog", ["hot","dot","dog","lot","log"]) == 0

    # Test 3: Direct transformation
    assert sol.ladder_length("hot", "dot", ["hot","dot","dog"]) == 2

    # Test 4: No path exists
    assert sol.ladder_length("a", "c", ["a","b","c"]) == 2

    # Test 5: Longer chain
    assert sol.ladder_length("hit", "cog", ["hot","dot","dog","lot","log","cog"]) == 5

    # Test 6: Single character change
    assert sol.ladder_length("cat", "hat", ["cat","hat"]) == 2

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
