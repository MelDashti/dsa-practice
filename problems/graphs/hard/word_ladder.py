"""
PROBLEM: Word Ladder (LeetCode 127)
LeetCode: https://leetcode.com/problems/word-ladder/
Difficulty: Hard
Pattern: Graphs (BFS)
Companies: Amazon, Google, Facebook, Microsoft, LinkedIn

A transformation sequence from word begin_word to word end_word using a dictionary word_list
is a sequence of words begin_word -> s1 -> s2 -> ... -> sk such that:
- Every adjacent pair of words differs by a single letter
- Every si for 1 <= i <= k is in word_list. Note that begin_word does not need to be in word_list
- sk == end_word

Given two words, begin_word and end_word, and a dictionary word_list, return the number of words
in the shortest transformation sequence from begin_word to end_word, or 0 if no such sequence exists.

Example 1:
    Input: begin_word = "hit", end_word = "cog", word_list = ["hot","dot","dog","lot","log","cog"]
    Output: 5
    Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> "cog",
    which is 5 words long.

Example 2:
    Input: begin_word = "hit", end_word = "cog", word_list = ["hot","dot","dog","lot","log"]
    Output: 0
    Explanation: The end_word "cog" is not in word_list, therefore there is no valid transformation sequence.

Constraints:
- 1 <= begin_word.length <= 10
- end_word.length == begin_word.length
- 1 <= word_list.length <= 5000
- word_list[i].length == begin_word.length
- begin_word, end_word, and word_list[i] consist of lowercase English letters
- begin_word != end_word
- All the words in word_list are unique

Approach:
1. Use BFS to find shortest path from begin_word to end_word
2. For each word, try changing each character to find valid next words
3. Only visit words that are in word_list
4. Track visited words to avoid cycles
5. Return level (number of transformations + 1) when end_word is found

Time: O(M^2 * N) - M is word length, N is number of words
Space: O(M * N) - queue and visited set
"""

from typing import List
from collections import deque


class Solution:
    def ladder_length(self, begin_word: str, end_word: str, word_list: List[str]) -> int:
        if end_word not in word_list:
            return 0

        # Convert to set for O(1) lookup
        word_set = set(word_list)
        queue = deque([(begin_word, 1)])  # (word, level)
        visited = {begin_word}

        while queue:
            word, level = queue.popleft()

            # Check if we reached the end
            if word == end_word:
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

    # Test 2: EndWord not in word_list
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
