"""
PROBLEM: N-Queens (LeetCode 51)
Difficulty: Hard
Pattern: Backtracking
Companies: Amazon, Microsoft, Facebook, Apple, Google

The n-queens puzzle is the problem of placing n queens on an n x n chessboard
such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. You
may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens'
placement, where 'Q' and '.' both indicate a queen and an empty space,
respectively.

Example 1:
    Input: n = 4
    Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
    Explanation: There exist two distinct solutions to the 4-queens puzzle

Example 2:
    Input: n = 1
    Output: [["Q"]]

Constraints:
- 1 <= n <= 9

Approach:
1. Use backtracking to place queens row by row
2. For each row, try placing queen in each column
3. Check if placement is valid (no conflicts with previous queens)
4. A queen attacks same row, column, and diagonals
5. Track used columns, positive diagonals (row+col), negative diagonals (row-col)
6. Base case: when all rows filled, add board configuration to result
7. Backtrack by removing queen and trying next position

Time: O(n!) - pruning makes it better than O(n^n)
Space: O(n^2) - board storage and recursion depth
"""

from typing import List


class Solution:
    def solve_n_queens(self, n: int) -> List[List[str]]:
        result = []
        board = [['.'] * n for _ in range(n)]

        # Sets to track attacked columns and diagonals
        cols = set()
        pos_diag = set()  # (row + col) is constant for positive diagonals
        neg_diag = set()  # (row - col) is constant for negative diagonals

        def backtrack(row):
            # Base case: placed all queens
            if row == n:
                result.append([''.join(row) for row in board])
                return

            # Try placing queen in each column of current row
            for col in range(n):
                # Check if position is under attack
                if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                    continue

                # Place queen
                board[row][col] = 'Q'
                cols.add(col)
                pos_diag.add(row + col)
                neg_diag.add(row - col)

                # Recurse to next row
                backtrack(row + 1)

                # Backtrack: remove queen
                board[row][col] = '.'
                cols.remove(col)
                pos_diag.remove(row + col)
                neg_diag.remove(row - col)

        backtrack(0)
        return result


# Tests
def test():
    sol = Solution()

    # Test case 1
    result1 = sol.solve_n_queens(4)
    expected1 = [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
    assert sorted(result1) == sorted(expected1)

    # Test case 2
    result2 = sol.solve_n_queens(1)
    expected2 = [["Q"]]
    assert result2 == expected2

    # Test case 3 - n=2 and n=3 have no solutions
    result3 = sol.solve_n_queens(2)
    assert result3 == []

    # Test case 4
    result4 = sol.solve_n_queens(8)
    assert len(result4) == 92  # There are 92 solutions for 8-queens

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
