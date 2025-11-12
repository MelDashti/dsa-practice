"""
PROBLEM: Word Search (LeetCode 79)
Difficulty: Medium
Pattern: Backtracking
Companies: Amazon, Microsoft, Facebook, Apple, Google

Given an m x n grid of characters board and a string word, return true if
word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells,
where adjacent cells are horizontally or vertically neighboring. The same
letter cell may not be used more than once.

Example 1:
    Input: board = [["A","B","C","E"],
                    ["S","F","C","S"],
                    ["A","D","E","E"]], word = "ABCCED"
    Output: true

Example 2:
    Input: board = [["A","B","C","E"],
                    ["S","F","C","S"],
                    ["A","D","E","E"]], word = "SEE"
    Output: true

Example 3:
    Input: board = [["A","B","C","E"],
                    ["S","F","C","S"],
                    ["A","D","E","E"]], word = "ABCB"
    Output: false

Constraints:
- m == board.length
- n = board[i].length
- 1 <= m, n <= 6
- 1 <= word.length <= 15
- board and word consists of only lowercase and uppercase English letters

Approach:
1. For each cell in the grid, try starting the search from there
2. Use DFS/backtracking to explore all possible paths
3. Mark current cell as visited (modify in place or use visited set)
4. Check all 4 directions (up, down, left, right)
5. If we match all characters in word, return true
6. Backtrack by unmarking the cell as visited
7. If no path found from any starting cell, return false

Time: O(m * n * 4^L) where L is length of word, 4 directions at each step
Space: O(L) - recursion depth
"""

from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        if not board or not board[0]:
            return False

        rows, cols = len(board), len(board[0])

        def backtrack(row, col, index):
            # Base case: found entire word
            if index == len(word):
                return True

            # Check boundaries
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False

            # Check if current cell matches and is not visited
            if board[row][col] != word[index]:
                return False

            # Mark as visited
            temp = board[row][col]
            board[row][col] = '#'

            # Explore all 4 directions
            found = (backtrack(row + 1, col, index + 1) or
                    backtrack(row - 1, col, index + 1) or
                    backtrack(row, col + 1, index + 1) or
                    backtrack(row, col - 1, index + 1))

            # Backtrack: unmark as visited
            board[row][col] = temp

            return found

        # Try starting from each cell
        for i in range(rows):
            for j in range(cols):
                if backtrack(i, j, 0):
                    return True

        return False


# Tests
def test():
    sol = Solution()

    # Test case 1
    board1 = [["A","B","C","E"],
              ["S","F","C","S"],
              ["A","D","E","E"]]
    assert sol.exist(board1, "ABCCED") == True

    # Test case 2
    board2 = [["A","B","C","E"],
              ["S","F","C","S"],
              ["A","D","E","E"]]
    assert sol.exist(board2, "SEE") == True

    # Test case 3
    board3 = [["A","B","C","E"],
              ["S","F","C","S"],
              ["A","D","E","E"]]
    assert sol.exist(board3, "ABCB") == False

    # Test case 4
    board4 = [["A"]]
    assert sol.exist(board4, "A") == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
