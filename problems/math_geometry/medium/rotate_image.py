"""
PROBLEM: Rotate Image (LeetCode 48)
LeetCode: https://leetcode.com/problems/rotate-image/
Difficulty: Medium
Pattern: Matrix, In-place, Rotation
Companies: Amazon, Apple, Facebook, Google, Microsoft

You are given an n x n 2D matrix representing an image. Rotate the image by 90 degrees
(clockwise).

You have to rotate the image in-place, which means you have to modify the input 2D matrix
directly. DO NOT allocate another 2D matrix and do the rotation.

Example 1:
    Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
    Output: [[7,4,1],[8,5,2],[9,6,3]]

Example 2:
    Input: matrix = [[5,1],[2,3]]
    Output: [[2,5],[3,1]]

Constraints:
- n == matrix.length == matrix[i].length
- 1 <= n <= 20
- -1000 <= matrix[i][j] <= 1000

Approach:
1. Transpose the matrix (swap matrix[i][j] with matrix[j][i])
2. Reverse each row of the transposed matrix
3. This achieves 90-degree clockwise rotation

Time: O(n^2) - visit each element once
Space: O(1) - in-place rotation
"""


class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        n = len(matrix)

        # Step 1: Transpose the matrix
        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        # Step 2: Reverse each row
        for i in range(n):
            matrix[i].reverse()


# Tests
def test():
    sol = Solution()

    # Test 1
    matrix1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    sol.rotate(matrix1)
    assert matrix1 == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

    # Test 2
    matrix2 = [[5, 1], [2, 3]]
    sol.rotate(matrix2)
    assert matrix2 == [[2, 5], [3, 1]]

    # Test 3
    matrix3 = [[1]]
    sol.rotate(matrix3)
    assert matrix3 == [[1]]

    # Test 4
    matrix4 = [[1, 2], [3, 4]]
    sol.rotate(matrix4)
    assert matrix4 == [[3, 1], [4, 2]]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
