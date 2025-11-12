"""
PROBLEM: Spiral Matrix (LeetCode 54)
Difficulty: Medium
Pattern: Matrix Traversal, Simulation
Companies: Amazon, Apple, Bloomberg, Facebook, Google, Microsoft

Given an m x n matrix, return all elements of the matrix in spiral order.

Example 1:
    Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
    Output: [1,2,3,6,9,8,7,4,5]

Example 2:
    Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    Output: [1,2,3,4,8,12,11,10,9,5,6,7]

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 10
- -100 <= matrix[i][j] <= 100

Approach:
1. Define boundaries: top, bottom, left, right
2. Traverse in spiral order:
   - Left to right along top row
   - Top to bottom along right column
   - Right to left along bottom row (if still rows left)
   - Bottom to top along left column (if still columns left)
3. Update boundaries after each direction
4. Continue until all elements are visited

Time: O(m * n) - visit each element once
Space: O(1) - not counting output array
"""


class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        if not matrix or not matrix[0]:
            return []

        m, n = len(matrix), len(matrix[0])
        result = []
        top, bottom, left, right = 0, m - 1, 0, n - 1

        while top <= bottom and left <= right:
            # Traverse right along top row
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1

            # Traverse down along right column
            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1

            # Traverse left along bottom row (if row exists)
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1

            # Traverse up along left column (if column exists)
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1

        return result


# Tests
def test():
    sol = Solution()

    # Test 1
    matrix1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert sol.spiralOrder(matrix1) == [1, 2, 3, 6, 9, 8, 7, 4, 5]

    # Test 2
    matrix2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    assert sol.spiralOrder(matrix2) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]

    # Test 3
    matrix3 = [[1]]
    assert sol.spiralOrder(matrix3) == [1]

    # Test 4
    matrix4 = [[1, 2, 3]]
    assert sol.spiralOrder(matrix4) == [1, 2, 3]

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
