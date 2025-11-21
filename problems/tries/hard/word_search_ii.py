"""
PROBLEM: Word Search II (212)
LeetCode: https://leetcode.com/problems/word-search-ii/
Difficulty: Hard
Pattern: Tries/Prefix Trees + Backtracking

Given an m x n board of characters and a list of strings words, return all words
on the board. Each word must be constructed from letters of sequentially adjacent cells,
where adjacent cells are horizontally or vertically neighbors.
The same letter cell may not be used more than once in one word.

Requirements:
- search(board, words): Find all words from the list that exist on the board
- Words are formed by moving to adjacent cells (4-directional)
- Each cell can only be used once per word
- Return list of found words

Example:
    board = [["o","a","a"],["e","t","a"],["t","a","f"]]
    words = ["oath","pea","eat","rain"]
    Output: ["eat","oath"]

Approach:
- Build a Trie from all words
- For each cell, use DFS/backtracking to find words
- Track visited cells to avoid reuse within a word
- Use Trie to prune search space

Time Complexity: O(M * N * 4^L * N_words) where M,N are board dimensions, L is max word length
Space Complexity: O(N_words * L) for Trie + O(M * N) for visited cells
"""


class TrieNode:
    """Node in the Trie structure for word search."""
    def __init__(self):
        self.children = {}
        self.word = None  # Store the word at leaf nodes


class WordSearchII:
    """Find all words from a list that exist on a 2D board."""

    def __init__(self):
        self.root = TrieNode()
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    def find_words(self, board: list[list[str]], words: list[str]) -> list[str]:
        """
        Find all words from the word list that exist on the board.

        Args:
            board: m x n grid of characters
            words: List of words to search for

        Returns:
            List of words found on the board
        """
        # Build Trie from all words
        for word in words:
            self._add_to_trie(word)

        result = []
        visited = [[False] * len(board[0]) for _ in range(len(board))]

        # Search for words from each cell
        for i in range(len(board)):
            for j in range(len(board[0])):
                self._dfs(board, i, j, visited, self.root, result)

        return result

    def _add_to_trie(self, word: str) -> None:
        """
        Add a word to the Trie.

        Args:
            word: Word to add to Trie
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word

    def _dfs(
        self,
        board: list[list[str]],
        row: int,
        col: int,
        visited: list[list[bool]],
        node: TrieNode,
        result: list[str],
    ) -> None:
        """
        DFS/backtracking to find words on the board.

        Args:
            board: m x n grid of characters
            row: Current row position
            col: Current column position
            visited: 2D array tracking visited cells
            node: Current Trie node
            result: List to store found words
        """
        # Get current character
        char = board[row][col]

        # Check if character exists in Trie
        if char not in node.children:
            return

        # Move to next Trie node
        next_node = node.children[char]

        # If we found a word, add it to result
        if next_node.word is not None:
            result.append(next_node.word)
            next_node.word = None  # Avoid duplicates

        # Mark as visited
        visited[row][col] = True

        # Explore all 4 directions
        for dr, dc in self.directions:
            new_row, new_col = row + dr, col + dc

            # Check bounds and visited
            if (
                0 <= new_row < len(board)
                and 0 <= new_col < len(board[0])
                and not visited[new_row][new_col]
            ):
                self._dfs(board, new_row, new_col, visited, next_node, result)

        # Backtrack
        visited[row][col] = False


# Tests
def test():
    # Test case 1: Simple horizontal word
    board1 = [["c", "a", "t"]]
    words1 = ["cat", "car", "card"]
    searcher1 = WordSearchII()
    result1 = searcher1.find_words(board1, words1)
    assert set(result1) == {"cat"}

    # Test case 2: Vertical word
    board2 = [["c"], ["a"], ["t"]]
    words2 = ["cat", "car"]
    searcher2 = WordSearchII()
    result2 = searcher2.find_words(board2, words2)
    assert set(result2) == {"cat"}

    # Test case 3: No words found
    board3 = [["a", "b"], ["c", "d"]]
    words3 = ["abcd", "dcba"]
    searcher3 = WordSearchII()
    result3 = searcher3.find_words(board3, words3)
    assert result3 == []

    # Test case 4: Multiple words with shared prefix
    board4 = [["a", "b"], ["a", "a"]]
    words4 = ["aa", "aaa", "aab"]
    searcher4 = WordSearchII()
    result4 = searcher4.find_words(board4, words4)
    assert set(result4) == {"aa", "aaa", "aab"}

    # Test case 5: Single cell board
    board5 = [["a"]]
    words5 = ["a", "b"]
    searcher5 = WordSearchII()
    result5 = searcher5.find_words(board5, words5)
    assert set(result5) == {"a"}

    # Test case 6: Non-adjacent words not found
    board6 = [["a", "b"], ["c", "d"]]
    words6 = ["ad", "bc"]
    searcher6 = WordSearchII()
    result6 = searcher6.find_words(board6, words6)
    # ad: a[0,0] not adjacent to d[1,1] (diagonal)
    # bc: b[0,1] not adjacent to c[1,0] (diagonal)
    assert result6 == []

    # Test case 7: 3x3 board with multiple words
    board7 = [["d", "o", "a"], ["r", "l", "e"], ["w", "l", "d"]]
    words7 = ["dole", "led", "door"]
    searcher7 = WordSearchII()
    result7 = searcher7.find_words(board7, words7)
    # dole: d[0,0]->o[0,1]->l[1,1]->e[1,2] ✓
    # led: l[1,1]->e[1,2]->d[2,2] ✓
    # door: d->o->o->r (need two o's adjacent, we only have one)
    assert set(result7) == {"dole", "led"}

    # Test case 8: Larger board with word reuse constraints
    board8 = [["a", "b"], ["a", "a"]]
    words8 = ["aaa", "aba", "baa"]
    searcher8 = WordSearchII()
    result8 = searcher8.find_words(board8, words8)
    # aaa: a[0,0]->a[1,0]->a[1,1] (valid)
    # aba: a[0,0]->b[0,1]->a[1,1] (valid)
    # baa: b[0,1]->a[0,0]->a[1,0] or b[0,1]->a[1,1]->a[1,0] (valid)
    assert set(result8) == {"aaa", "aba", "baa"}

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
