"""
PROBLEM: Number of Islands (LeetCode 200)
LeetCode: https://leetcode.com/problems/number-of-islands/
Difficulty: Medium
Pattern: Graphs (DFS/BFS)
Companies: Amazon, Facebook, Google, Microsoft, Bloomberg

Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water),
return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally
or vertically. You may assume all four edges of the grid are all surrounded by water.

Example 1:
    Input: grid = [
      ["1","1","1","1","0"],
      ["1","1","0","1","0"],
      ["1","1","0","0","0"],
      ["0","0","0","0","0"]
    ]
    Output: 1

Example 2:
    Input: grid = [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
    Output: 3

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 300
- grid[i][j] is '0' or '1'

Approach:
1. Iterate through each cell in the grid
2. When we find a '1', increment island count
3. Use DFS/BFS to mark all connected land cells as visited
4. Continue until all cells are processed

Time: O(m * n) - visit each cell once
Space: O(m * n) - recursion stack in worst case
"""

from typing import List


class Solution:
    def num_islands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands = 0

        def dfs(r, c):
            # Check bounds and if it's water or already visited
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                grid[r][c] == '0'):
                return

            # Mark as visited by changing to '0'
            grid[r][c] = '0'

            # Explore all 4 directions
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # Iterate through each cell
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    islands += 1
                    dfs(r, c)

        return islands


# Tests
def test():
    sol = Solution()

    # Test 1: Single island
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    assert sol.num_islands(grid1) == 1

    # Test 2: Multiple islands
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    assert sol.num_islands(grid2) == 3

    # Test 3: No islands
    grid3 = [
        ["0","0","0"],
        ["0","0","0"]
    ]
    assert sol.num_islands(grid3) == 0

    # Test 4: All land
    grid4 = [
        ["1","1"],
        ["1","1"]
    ]
    assert sol.num_islands(grid4) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
