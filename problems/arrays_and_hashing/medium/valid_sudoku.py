"""
PROBLEM: Valid Sudoku (LeetCode 36)
Difficulty: Medium
Pattern: Arrays & Hashing
Companies: Amazon, Apple, Google, Microsoft, Uber

Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be
validated according to the following rules:

1. Each row must contain the digits 1-9 without repetition.
2. Each column must contain the digits 1-9 without repetition.
3. Each of the nine 3 x 3 sub-boxes must contain the digits 1-9 without repetition.

Note: A Sudoku board (partially filled) could be valid but is not necessarily solvable.

Example 1:
    Input: board =
    [["5","3",".",".","7",".",".",".","."]
    ,["6",".",".","1","9","5",".",".","."]
    ,[".","9","8",".",".",".",".","6","."]
    ,["8",".",".",".","6",".",".",".","3"]
    ,["4",".",".","8",".","3",".",".","1"]
    ,["7",".",".",".","2",".",".",".","6"]
    ,[".","6",".",".",".",".","2","8","."]
    ,[".",".",".","4","1","9",".",".","5"]
    ,[".",".",".",".","8",".",".","7","9"]]
    Output: true

Example 2:
    Input: board =
    [["8","3",".",".","7",".",".",".","."]
    ,["6",".",".","1","9","5",".",".","."]
    ,[".","9","8",".",".",".",".","6","."]
    ,["8",".",".",".","6",".",".",".","3"]
    ,["4",".",".","8",".","3",".",".","1"]
    ,["7",".",".",".","2",".",".",".","6"]
    ,[".","6",".",".",".",".","2","8","."]
    ,[".",".",".","4","1","9",".",".","5"]
    ,[".",".",".",".","8",".",".","7","9"]]
    Output: false

Approach:
1. Use sets to track seen numbers in rows, columns, and boxes
2. For each cell, check if number already exists in its row/col/box
3. Box index = (row // 3, col // 3)

Time: O(1) - fixed 9x9 board
Space: O(1) - fixed size sets
"""

from typing import List
from collections import defaultdict


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = defaultdict(set)
        cols = defaultdict(set)
        boxes = defaultdict(set)

        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    continue

                num = board[r][c]

                # Check if number already exists in row, column, or box
                if (num in rows[r] or
                    num in cols[c] or
                    num in boxes[(r // 3, c // 3)]):
                    return False

                # Add number to respective sets
                rows[r].add(num)
                cols[c].add(num)
                boxes[(r // 3, c // 3)].add(num)

        return True


# Tests
def test():
    sol = Solution()

    board1 = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    assert sol.isValidSudoku(board1) == True

    board2 = [
        ["8","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    assert sol.isValidSudoku(board2) == False

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
