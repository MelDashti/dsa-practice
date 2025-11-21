"""
PROBLEM: Rotting Oranges (LeetCode 994)
Difficulty: Medium
Pattern: Graphs (BFS)
Companies: Amazon, Microsoft, Bloomberg, Facebook, Google

You are given an m x n grid where each cell can have one of three values:
- 0 representing an empty cell,
- 1 representing a fresh orange, or
- 2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange
becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange.
If this is impossible, return -1.

Example 1:
    Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
    Output: 4

Example 2:
    Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
    Output: -1
    Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten,
    because rotting only happens 4-directionally.

Example 3:
    Input: grid = [[0,2]]
    Output: 0
    Explanation: Since there are already no fresh oranges at minute 0, the answer is 0.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 10
- grid[i][j] is 0, 1, or 2

Approach:
1. Use BFS starting from all rotten oranges simultaneously
2. Count fresh oranges initially
3. Process level by level (each level = 1 minute)
4. Mark fresh oranges as rotten when visited
5. If fresh oranges remain after BFS, return -1

Time: O(m * n) - visit each cell once
Space: O(m * n) - queue in worst case
"""

from typing import List
from collections import deque


class Solution:
    def oranges_rotting(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return -1

        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh = 0
        minutes = 0

        # Count fresh oranges and add rotten oranges to queue
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    fresh += 1
                elif grid[r][c] == 2:
                    queue.append((r, c))

        # If no fresh oranges, return 0
        if fresh == 0:
            return 0

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # BFS
        while queue and fresh > 0:
            minutes += 1
            for _ in range(len(queue)):
                r, c = queue.popleft()

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc

                    # Check bounds and if it's a fresh orange
                    if (0 <= nr < rows and 0 <= nc < cols and
                        grid[nr][nc] == 1):
                        grid[nr][nc] = 2
                        fresh -= 1
                        queue.append((nr, nc))

        return minutes if fresh == 0 else -1


# Tests
def test():
    sol = Solution()

    # Test 1: All oranges rot
    grid1 = [[2,1,1],[1,1,0],[0,1,1]]
    assert sol.oranges_rotting(grid1) == 4

    # Test 2: Impossible to rot all
    grid2 = [[2,1,1],[0,1,1],[1,0,1]]
    assert sol.oranges_rotting(grid2) == -1

    # Test 3: No fresh oranges
    grid3 = [[0,2]]
    assert sol.oranges_rotting(grid3) == 0

    # Test 4: All fresh, no rotten
    grid4 = [[1,1,1],[1,1,1]]
    assert sol.oranges_rotting(grid4) == -1

    # Test 5: Single rotten orange
    grid5 = [[2]]
    assert sol.oranges_rotting(grid5) == 0

    print("✓ All tests passed")


if __name__ == "__main__":
    test()
