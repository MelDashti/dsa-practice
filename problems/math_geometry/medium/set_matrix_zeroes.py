"""
PROBLEM: Set Matrix Zeroes (LeetCode 73)
Difficulty: Medium
Pattern: Matrix, In-place, Hash Set
Companies: Amazon, Apple, Facebook, Google, Microsoft, Qualcomm

Given an m x n integer matrix matrix, if an element is 0, set its entire row and
column to 0's.

You must do it in-place.

Example 1:
    Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]
    Output: [[1,0,1],[0,0,0],[1,0,1]]

Example 2:
    Input: matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
    Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- -2^31 <= matrix[i][j] <= 2^31 - 1

Approach:
1. Store all row and column indices that contain zeros
2. Iterate through matrix and set entire rows and columns to 0
3. Use two sets to track which rows and columns need to be zeroed

Time: O(m * n) - visit each element twice
Space: O(m + n) - for storing row and column indices
"""


class Solution:
    def set_zeroes(self, matrix: list[list[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        if not matrix or not matrix[0]:
            return

        m, n = len(matrix), len(matrix[0])
        rows = set()
        cols = set()

        # First pass: identify rows and columns with zeros
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    rows.add(i)
                    cols.add(j)

        # Second pass: set zeros
        for i in range(m):
            for j in range(n):
                if i in rows or j in cols:
                    matrix[i][j] = 0


# Tests
def test():
    sol = Solution()

    # Test 1
    matrix1 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    sol.set_zeroes(matrix1)
    assert matrix1 == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

    # Test 2
    matrix2 = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    sol.set_zeroes(matrix2)
    assert matrix2 == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]

    # Test 3
    matrix3 = [[1, 1], [1, 1]]
    sol.set_zeroes(matrix3)
    assert matrix3 == [[1, 1], [1, 1]]

    # Test 4
    matrix4 = [[0]]
    sol.set_zeroes(matrix4)
    assert matrix4 == [[0]]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
