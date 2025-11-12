"""
PROBLEM: Max Area of Island (LeetCode 695)
Difficulty: Medium
Pattern: Graphs (DFS/BFS)
Companies: Amazon, Facebook, Google, Microsoft

You are given an m x n binary matrix grid. An island is a group of 1's (representing land)
connected 4-directionally (horizontal or vertical). You may assume all four edges of the
grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.

Example 1:
    Input: grid = [
        [0,0,1,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,1,1,0,1,0,0,0,0,0,0,0,0],
        [0,1,0,0,1,1,0,0,1,0,1,0,0],
        [0,1,0,0,1,1,0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0,0,0]
    ]
    Output: 6
    Explanation: The answer is not 11, because the island must be connected 4-directionally.

Example 2:
    Input: grid = [[0,0,0,0,0,0,0,0]]
    Output: 0

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- grid[i][j] is either 0 or 1

Approach:
1. Iterate through each cell in the grid
2. When we find a 1, use DFS to calculate the area of that island
3. Mark visited cells as 0 to avoid revisiting
4. Track the maximum area found
5. Return the maximum area

Time: O(m * n) - visit each cell once
Space: O(m * n) - recursion stack in worst case
"""

from typing import List


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        max_area = 0

        def dfs(r, c):
            # Check bounds and if it's water or already visited
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                grid[r][c] == 0):
                return 0

            # Mark as visited
            grid[r][c] = 0

            # Count current cell + all connected cells
            area = 1
            area += dfs(r + 1, c)
            area += dfs(r - 1, c)
            area += dfs(r, c + 1)
            area += dfs(r, c - 1)

            return area

        # Iterate through each cell
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    max_area = max(max_area, dfs(r, c))

        return max_area


# Tests
def test():
    sol = Solution()

    # Test 1: Grid with islands of different sizes
    grid1 = [
        [0,0,1,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,1,1,0,1,0,0,0,0,0,0,0,0],
        [0,1,0,0,1,1,0,0,1,0,1,0,0],
        [0,1,0,0,1,1,0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,1,1,0,0,0,0]
    ]
    assert sol.maxAreaOfIsland(grid1) == 6

    # Test 2: No islands
    grid2 = [[0,0,0,0,0,0,0,0]]
    assert sol.maxAreaOfIsland(grid2) == 0

    # Test 3: All land
    grid3 = [[1,1],[1,1]]
    assert sol.maxAreaOfIsland(grid3) == 4

    # Test 4: Single cell island
    grid4 = [[0,0,0],[0,1,0],[0,0,0]]
    assert sol.maxAreaOfIsland(grid4) == 1

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
