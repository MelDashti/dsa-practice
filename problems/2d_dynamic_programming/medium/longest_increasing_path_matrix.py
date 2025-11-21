"""
PROBLEM: Longest Increasing Path in a Matrix (LeetCode 329)
LeetCode: https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
Difficulty: Hard
Pattern: 2-D Dynamic Programming
Companies: Amazon, Google, Microsoft, Facebook, Apple

Given an m x n integers matrix, return the length of the longest increasing path
in matrix.

From each cell, you can either move in four directions: left, right, up, or down.
You may not move diagonally or move outside the boundary (i.e., wrap-around is
not allowed).

Example 1:
    Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
    Output: 4
    Explanation: The longest increasing path is [1, 2, 6, 9].

Example 2:
    Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
    Output: 4
    Explanation: The longest increasing path is [3, 4, 5, 6]. Moving diagonally
    is not allowed.

Example 3:
    Input: matrix = [[1]]
    Output: 1

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 200
- 0 <= matrix[i][j] <= 2^31 - 1

Approach:
1. Use DFS with memoization (top-down DP)
2. For each cell, try all 4 directions
3. Only move to cells with larger values (increasing path)
4. Cache the longest path from each cell to avoid recomputation
5. Answer is max of all starting positions

Time: O(m * n) - visit each cell once due to memoization
Space: O(m * n) - memoization cache and recursion stack
"""

from typing import List


class Solution:
    def longest_increasing_path(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        memo = {}

        def dfs(i: int, j: int) -> int:
            # Return cached result if available
            if (i, j) in memo:
                return memo[(i, j)]

            # Start with length 1 (the cell itself)
            max_length = 1

            # Try all 4 directions
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj

                # Check bounds and increasing condition
                if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] > matrix[i][j]:
                    max_length = max(max_length, 1 + dfs(ni, nj))

            # Cache and return result
            memo[(i, j)] = max_length
            return max_length

        # Try starting from every cell
        result = 0
        for i in range(m):
            for j in range(n):
                result = max(result, dfs(i, j))

        return result


# Tests
def test():
    sol = Solution()

    assert sol.longest_increasing_path([[9,9,4],[6,6,8],[2,1,1]]) == 4
    assert sol.longest_increasing_path([[3,4,5],[3,2,6],[2,2,1]]) == 4
    assert sol.longest_increasing_path([[1]]) == 1
    assert sol.longest_increasing_path([[1,2]]) == 2
    assert sol.longest_increasing_path([[7,8,9],[9,7,6],[7,2,3]]) == 6

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
