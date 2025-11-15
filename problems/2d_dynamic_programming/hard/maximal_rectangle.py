"""
PROBLEM: Maximal Rectangle (LeetCode 85)
Difficulty: Hard
Pattern: 2-D Dynamic Programming, Monotonic Stack
Companies: Amazon, Google, Meta, Apple

DESCRIPTION:
Given a rows x cols binary matrix filled with 0's and 1's, find the largest
rectangle containing only 1's and return its area.

EXAMPLES:
Example 1:
Input: matrix = [
  ["1","0","1","0","0"],
  ["1","0","1","1","1"],
  ["1","1","1","1","1"],
  ["1","0","0","1","0"]
]
Output: 6
Explanation: The maximal rectangle is:
1 1 1
1 1 1

Example 2:
Input: matrix = [["0"]]
Output: 0

Example 3:
Input: matrix = [["1"]]
Output: 1

CONSTRAINTS:
- rows == matrix.length
- cols == matrix[i].length
- 1 <= rows, cols <= 200
- matrix[i][j] is '0' or '1'

APPROACH:
This is an extension of "Largest Rectangle in Histogram" (LeetCode 84).

For each row, treat it as the base of a histogram where:
- Heights[j] = number of consecutive 1's above (including current row)
- Apply "Largest Rectangle in Histogram" algorithm for each row

Algorithm:
1. Build histogram heights for each row
2. For each row, find largest rectangle using monotonic stack
3. Track maximum area across all rows

TIME COMPLEXITY: O(rows × cols)
- O(rows) iterations, each doing O(cols) histogram calculation

SPACE COMPLEXITY: O(cols)
- Heights array and stack

WHY THIS PROBLEM IS IMPORTANT:
- Combines 2-D DP with Monotonic Stack
- Frequently asked at Amazon and Google (especially for SDE2+)
- Tests ability to reduce 2-D problem to 1-D
- Builds on "Largest Rectangle in Histogram" problem
"""

from typing import List


class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        """
        Find maximal rectangle in binary matrix using histogram approach.
        """
        if not matrix or not matrix[0]:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        heights = [0] * cols
        max_area = 0

        for row in range(rows):
            # Update heights for current row
            for col in range(cols):
                if matrix[row][col] == '1':
                    heights[col] += 1
                else:
                    heights[col] = 0

            # Find largest rectangle in current histogram
            max_area = max(max_area, self.largestRectangleArea(heights))

        return max_area

    def largestRectangleArea(self, heights: List[int]) -> int:
        """
        Find largest rectangle in histogram using monotonic stack.
        """
        stack = []  # Store indices
        max_area = 0
        heights.append(0)  # Add sentinel to flush stack

        for i in range(len(heights)):
            # Maintain increasing stack
            while stack and heights[i] < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, h * w)

            stack.append(i)

        heights.pop()  # Remove sentinel
        return max_area


class SolutionDP:
    """
    Alternative DP approach without using stack.
    """

    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        """
        DP approach tracking left, right, and height boundaries.
        """
        if not matrix or not matrix[0]:
            return 0

        rows, cols = len(matrix), len(matrix[0])

        # For each cell, track:
        # heights[j] = consecutive 1's above (including current)
        # left[j] = leftmost index we can extend to
        # right[j] = rightmost index we can extend to
        heights = [0] * cols
        left = [0] * cols
        right = [cols] * cols

        max_area = 0

        for i in range(rows):
            curr_left = 0  # Leftmost 1 in current row
            curr_right = cols  # Rightmost 1 in current row

            # Update heights and left boundaries
            for j in range(cols):
                if matrix[i][j] == '1':
                    heights[j] += 1
                    left[j] = max(left[j], curr_left)
                else:
                    heights[j] = 0
                    left[j] = 0
                    curr_left = j + 1

            # Update right boundaries (right to left)
            for j in range(cols - 1, -1, -1):
                if matrix[i][j] == '1':
                    right[j] = min(right[j], curr_right)
                else:
                    right[j] = cols
                    curr_right = j

            # Calculate areas
            for j in range(cols):
                max_area = max(max_area, heights[j] * (right[j] - left[j]))

        return max_area


def test_maximal_rectangle():
    """Test cases for Maximal Rectangle"""
    solutions = [Solution(), SolutionDP()]

    test_cases = [
        (
            [
                ["1", "0", "1", "0", "0"],
                ["1", "0", "1", "1", "1"],
                ["1", "1", "1", "1", "1"],
                ["1", "0", "0", "1", "0"],
            ],
            6,
        ),
        ([["0"]], 0),
        ([["1"]], 1),
        ([["0", "0"]], 0),
        ([["1", "1"], ["1", "1"]], 4),
        (
            [["1", "1", "1"], ["1", "1", "1"], ["1", "1", "1"]],
            9,
        ),
        ([["1", "0", "1"], ["1", "1", "1"], ["1", "0", "1"]], 4),
    ]

    for sol in solutions:
        for matrix, expected in test_cases:
            # Deep copy matrix for each solution
            matrix_copy = [row[:] for row in matrix]
            result = sol.maximalRectangle(matrix_copy)
            assert (
                result == expected
            ), f"{sol.__class__.__name__} failed: got {result}, expected {expected}"

    print("✅ All test cases passed for all solutions!")


if __name__ == "__main__":
    test_maximal_rectangle()
