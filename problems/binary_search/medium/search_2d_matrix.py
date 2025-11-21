"""
PROBLEM: Search a 2D Matrix (LeetCode 74)
LeetCode: https://leetcode.com/problems/search-a-2d-matrix/
Difficulty: Medium
Pattern: Binary Search
Companies: Amazon, Microsoft, Google, Facebook, Apple

You are given an m x n integer matrix matrix with the following two properties:
- Each row is sorted in non-decreasing order
- The first integer of each row is greater than the last integer of the previous row

Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.

Example 1:
    Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
    Output: true

Example 2:
    Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
    Output: false

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 100
- -10^4 <= matrix[i][j], target <= 10^4

Approach:
1. Treat the 2D matrix as a sorted 1D array
2. Use binary search on virtual 1D array
3. Convert 1D index to 2D coordinates: row = idx // cols, col = idx % cols
4. Search for target using standard binary search

Time: O(log(m * n)) - binary search on m*n elements
Space: O(1) - only using pointers
"""

from typing import List


class Solution:
    def search_matrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or not matrix[0]:
            return False

        m, n = len(matrix), len(matrix[0])
        left, right = 0, m * n - 1

        while left <= right:
            mid = left + (right - left) // 2
            # Convert 1D index to 2D coordinates
            row, col = mid // n, mid % n
            mid_value = matrix[row][col]

            if mid_value == target:
                return True
            elif mid_value < target:
                left = mid + 1
            else:
                right = mid - 1

        return False


# Tests
def test():
    sol = Solution()

    assert sol.search_matrix([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3) == True
    assert sol.search_matrix([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 13) == False
    assert sol.search_matrix([[1]], 1) == True
    assert sol.search_matrix([[1]], 2) == False
    assert sol.search_matrix([[1,3]], 3) == True
    assert sol.search_matrix([[1],[3]], 3) == True

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
