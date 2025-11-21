"""
PROBLEM: Surrounded Regions (LeetCode 130)
LeetCode: https://leetcode.com/problems/surrounded-regions/
Difficulty: Medium
Pattern: Graphs (DFS/BFS)
Companies: Amazon, Google, Facebook, Microsoft, Bloomberg

Given an m x n matrix board containing 'X' and 'O', capture all regions that are
4-directionally surrounded by 'X'.

A region is captured by flipping all 'O's into 'X's in that surrounded region.

Example 1:
    Input: board = [
        ["X","X","X","X"],
        ["X","O","O","X"],
        ["X","X","O","X"],
        ["X","O","X","X"]
    ]
    Output: [
        ["X","X","X","X"],
        ["X","X","X","X"],
        ["X","X","X","X"],
        ["X","O","X","X"]
    ]
    Explanation: Notice that an 'O' should not be flipped if:
    - It is on the border, or
    - It is adjacent to an 'O' that should not be flipped.
    The bottom 'O' is on the border, so it is not flipped, and the other two
    'O's in the second row are flipped.

Example 2:
    Input: board = [["X"]]
    Output: [["X"]]

Constraints:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 200
- board[i][j] is 'X' or 'O'

Approach:
1. Find all 'O's on the border
2. Mark them and their connected 'O's as safe (using DFS/BFS)
3. Flip all remaining 'O's to 'X's
4. Restore safe 'O's back

Time: O(m * n) - visit each cell at most twice
Space: O(m * n) - recursion stack in worst case
"""

from typing import List


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        if not board or not board[0]:
            return

        rows, cols = len(board), len(board[0])

        def dfs(r, c):
            # Check bounds and if it's not 'O'
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                board[r][c] != 'O'):
                return

            # Mark as safe (temporary marker)
            board[r][c] = 'T'

            # Explore all 4 directions
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # Mark all border-connected 'O's as safe
        # Top and bottom borders
        for c in range(cols):
            if board[0][c] == 'O':
                dfs(0, c)
            if board[rows - 1][c] == 'O':
                dfs(rows - 1, c)

        # Left and right borders
        for r in range(rows):
            if board[r][0] == 'O':
                dfs(r, 0)
            if board[r][cols - 1] == 'O':
                dfs(r, cols - 1)

        # Flip remaining 'O's to 'X' and restore 'T's to 'O'
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
                elif board[r][c] == 'T':
                    board[r][c] = 'O'


# Tests
def test():
    sol = Solution()

    # Test 1: Standard case
    board1 = [
        ["X","X","X","X"],
        ["X","O","O","X"],
        ["X","X","O","X"],
        ["X","O","X","X"]
    ]
    sol.solve(board1)
    expected1 = [
        ["X","X","X","X"],
        ["X","X","X","X"],
        ["X","X","X","X"],
        ["X","O","X","X"]
    ]
    assert board1 == expected1

    # Test 2: Single cell
    board2 = [["X"]]
    sol.solve(board2)
    assert board2 == [["X"]]

    # Test 3: All border O's
    board3 = [
        ["O","O","O"],
        ["O","X","O"],
        ["O","O","O"]
    ]
    sol.solve(board3)
    expected3 = [
        ["O","O","O"],
        ["O","X","O"],
        ["O","O","O"]
    ]
    assert board3 == expected3

    # Test 4: All surrounded
    board4 = [
        ["X","X","X"],
        ["X","O","X"],
        ["X","X","X"]
    ]
    sol.solve(board4)
    expected4 = [
        ["X","X","X"],
        ["X","X","X"],
        ["X","X","X"]
    ]
    assert board4 == expected4

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
